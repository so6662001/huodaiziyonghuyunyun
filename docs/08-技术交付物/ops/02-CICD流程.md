# CI/CD 流程

## 一、整体流程

```
开发者
   ↓ 推 Git
GitLab / GitHub
   ↓ 触发 Webhook
GitLab CI / GitHub Actions
   ↓ 多阶段流水线
   ├─ Lint / 单元测试
   ├─ 构建镜像
   ├─ 推到 ACR
   ├─ 部署 dev → test → staging → prod
   └─ 自动化测试 + 灰度
```

## 二、分支策略

```
main             生产分支（与生产环境同步）
develop          开发主分支
feature/*        功能分支
hotfix/*         紧急修复分支
release/v2.x.x   发布分支

工作流：
  feature/* ──→ develop（PR + Code Review）
  develop   ──→ release/v2.x.x（每两周）
  release/* ──→ main（验收通过后）
  hotfix/*  ──→ main + develop
```

## 三、CI 流水线

### 阶段 1：代码检查（5 分钟）

```yaml
stages:
  - name: lint
    steps:
      - eslint / golangci-lint / mvn validate
      - 提交信息格式检查（Conventional Commits）
      - 敏感词检查
  - name: security_scan
    steps:
      - 依赖漏洞扫描（npm audit / mvn dependency-check）
      - 静态代码安全扫描（SonarQube）
```

### 阶段 2：单元测试（10 分钟）

```yaml
- name: unit_test
  steps:
    - 后端：mvn test / go test
    - 前端：jest --coverage
    - 覆盖率门槛：核心模块 ≥ 80%
    - 失败即阻塞
```

### 阶段 3：构建（5 分钟）

```yaml
- name: build
  steps:
    - mvn package（Java）/ go build / npm build
    - 生成 Docker 镜像
    - 镜像安全扫描（Trivy）
    - 推送到 ACR（tag: sha-{commit_sha}）
```

### 阶段 4：集成测试（15 分钟）

```yaml
- name: integration_test
  on: merge_to_develop
  environment: test
  steps:
    - 部署到 test 环境
    - 运行集成测试用例
    - 失败回滚（保留 dev 环境状态）
```

### 阶段 5：E2E + 性能（30 分钟）

```yaml
- name: e2e_test
  on: pr_to_release
  environment: staging
  steps:
    - 部署到 staging
    - Playwright E2E（核心 11 个业务流）
    - k6 性能基线测试
    - 失败阻塞合并到 main
```

### 阶段 6：发布（手工触发）

```yaml
- name: deploy_prod
  on: manual + cto_approval
  steps:
    - 蓝绿部署（先小流量 5%）
    - 监控 30 分钟
    - 自动健康检查
    - 通过后切流量 50% → 100%
    - 失败自动回滚
```

## 四、Helm Chart 结构

```
helm/
├── Chart.yaml
├── values.yaml              # 默认配置
├── values-dev.yaml
├── values-test.yaml
├── values-staging.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── hpa.yaml
    └── pdb.yaml             # PodDisruptionBudget
```

### values-prod.yaml 关键配置

```yaml
replicaCount: 5

image:
  repository: registry.cn-beijing.aliyuncs.com/huodaizi/api
  tag: v2.0.0
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi

autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 30
  targetCPUUtilizationPercentage: 70

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app
              operator: In
              values:
                - api-service
        topologyKey: topology.kubernetes.io/zone

livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 20
  periodSeconds: 5
```

## 五、Argo CD 配置

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: huodaizi-prod
spec:
  source:
    repoURL: git@gitlab.com:huodaizi/helm.git
    targetRevision: main
    path: api-service
    helm:
      valueFiles:
        - values-prod.yaml
  destination:
    server: https://k8s-prod.huodaizi.com
    namespace: prod-app
  syncPolicy:
    automated:
      prune: false      # 不自动删除（手工 review）
      selfHeal: true    # 自动修复偏差
    syncOptions:
      - CreateNamespace=true
```

## 六、发布流程

### 1. 常规发布（每两周）

```
T-7  发布计划评审
T-5  从 develop 切 release/v2.x.x 分支
T-5  → staging 部署
T-4  staging E2E + 性能验证
T-3  staging 灰度验证（内部 30 人）
T-2  灰度生产（5% 流量）
T-1  灰度扩量（50%）
T+0  全量发布
T+1  发布后 24h 监控
T+3  发布回顾会
```

### 2. 紧急发布

```
触发：
  - 严重 bug
  - 安全漏洞
  - 数据问题

流程：
  T+0   从 main 切 hotfix 分支
  T+0   修复 + 单元测试
  T+10m CTO 批准
  T+15m staging 快速验证
  T+30m 生产灰度（10% → 50% → 100%）
  T+1h  完成发布
  T+24h 复盘
```

### 3. 回滚流程

```
触发条件：
  - 监控错误率 > 5%
  - P95 延迟 > 基线 × 2
  - 关键业务功能不可用

步骤：
  Step 1: Argo CD 一键回滚到上一版本
        kubectl rollout undo deployment/api-service
  Step 2: 数据库变更回滚（如有）
        Flyway undo
  Step 3: 通知全员
  Step 4: 复盘 + 修复
```

## 七、数据库迁移

### 1. Flyway 流程

```
migration/
├── V001__create_users.sql
├── V002__create_sessions.sql
├── V003__add_priority_to_session.sql
└── V004__add_index_to_dispatches.sql

执行：
  - 应用启动时自动执行
  - 每次只执行未应用的版本

回滚：
  - U001__rollback_users.sql（成对编写）
  - 不要在生产用 undo（用前向修复）
```

### 2. 数据库变更规范

| 操作 | 安全等级 | 备注 |
|---|---|---|
| 加字段（可空） | 安全 | 直接发 |
| 加字段（NOT NULL，有默认值） | 安全 | 但要选好默认值 |
| 加索引 | 中 | 用 `ALGORITHM=INPLACE` |
| 改字段类型 | 风险 | 需评估锁表时间 |
| 删字段 | 高风险 | 先发版隐藏 → 一周后再删 |
| 删表 | 高风险 | 先重命名 → 一周后再删 |

### 3. 大表变更（千万级）

```
工具：gh-ost / pt-online-schema-change

避免：
  - 长时间锁表
  - 主从延迟扩大

低峰执行：凌晨 2:00-5:00
```

## 八、配置变更

### Nacos 配置

```
配置变更不需要重启应用（实时生效）
但敏感配置变更必须：
  - CTO 审批
  - 灰度生效（按 IP 段）
  - 留痕

不允许在 Nacos 直接改：
  - 数据库连接（重启生效）
  - 第三方 API Key（需轮换）
```

## 九、CI/CD 监控

```
关键指标：
  - 构建时长 P95 < 15 分钟
  - 单元测试通过率 ≥ 98%
  - 集成测试通过率 ≥ 95%
  - E2E 通过率 ≥ 90%
  - 部署成功率 ≥ 95%
  - 平均发布频率：每周 1-2 次

故障：
  - 构建超时（> 30 分钟）→ 调查
  - 测试莫名失败 → 修复测试稳定性
  - 部署失败 → 立即回滚
```

## 十、工具链总结

| 用途 | 工具 |
|---|---|
| 代码仓库 | GitLab / GitHub |
| CI | GitLab CI / GitHub Actions |
| CD | Argo CD |
| 镜像仓库 | 阿里云 ACR |
| 配置中心 | Nacos |
| 数据库迁移 | Flyway |
| 镜像扫描 | Trivy |
| 静态扫描 | SonarQube |
| 安全扫描 | OWASP Dependency Check / Snyk |
| 制品管理 | Nexus / Harbor |
| 文档 | Confluence / Notion |

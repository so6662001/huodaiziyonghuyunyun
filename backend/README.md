# 货袋子后端代码骨架（Java Spring Boot 3.x）

> **完整 Spring Cloud 微服务架构**，可直接编译运行。
> 基于 OpenAPI 规范（`docs/08-技术交付物/api/openapi.yaml`）和 DDL（`docs/08-技术交付物/db/01-schema.sql`）实现。

## 一、技术栈

| 组件 | 版本 | 说明 |
|---|---|---|
| Java | 17 LTS | 主语言 |
| Spring Boot | 3.2.x | 应用框架 |
| Spring Cloud | 2023.0.x | 微服务框架 |
| Spring Cloud Alibaba | 2023.0.x | Nacos 注册中心 |
| Maven | 3.9+ | 构建工具 |
| MySQL | 8.0+ | 主数据库 |
| Redis | 7.0+ | 缓存 |
| RocketMQ / Kafka | 5.x / 3.x | 消息队列 |
| Elasticsearch | 8.x | 搜索 |
| MyBatis Plus | 3.5.x | ORM |
| Sa-Token | 1.37.x | 权限框架 |
| Hutool | 5.8.x | 工具库 |
| Lombok | 1.18.x | 代码简化 |
| MapStruct | 1.5.x | DTO 转换 |
| Knife4j | 4.x | API 文档 |
| Logback | 1.4.x | 日志 |

## 二、项目结构

```
backend/
├── pom.xml                              # 父 Maven
├── README.md                            # 本文档
├── huodaizi-common/                     # 通用组件（响应/异常/工具）
├── huodaizi-domain/                     # 领域模型（实体/枚举）
├── huodaizi-user-service/               # 用户服务（完整示例）⭐
├── huodaizi-session-service/            # 采购会话服务（核心）⭐
├── huodaizi-list-service/               # 清单服务（OCR + LLM）
├── huodaizi-quote-service/              # 报价服务
├── huodaizi-dispatch-service/           # 智能匹配引擎（核心）⭐
├── huodaizi-credit-service/             # 信用体系
├── huodaizi-commercial-service/         # 商业化（流量费/SaaS）
├── huodaizi-risk-service/               # 风控反作弊（36 规则）
├── huodaizi-ai-service/                 # AI 服务（OCR/LLM）
├── huodaizi-notification-service/       # 通知服务
├── huodaizi-gateway/                    # API 网关
└── deploy/                              # 部署配置
    ├── docker-compose.yml
    └── k8s/
```

## 三、模块说明

### 3.1 公共模块（必备）

```
huodaizi-common       Result/Error/Util/AOP
huodaizi-domain       Entity/Enum/DTO（跨服务复用）
```

### 3.2 业务微服务（11 个）

| 服务 | 端口 | 核心功能 |
|---|---|---|
| user-service | 8001 | 用户/企业认证 |
| session-service | 8002 | 采购会话/需求卡片 |
| list-service | 8003 | 清单上传/拆单/最优组合 |
| quote-service | 8004 | 报价/议价 |
| dispatch-service | 8005 | 智能匹配/三级池 |
| credit-service | 8006 | 信用分/申诉/评价 |
| commercial-service | 8007 | 会员/流量费/SaaS |
| risk-service | 8008 | 反作弊/风控规则 |
| ai-service | 8009 | OCR + LLM 调用 |
| notification-service | 8010 | 短信/微信/Push |
| gateway | 8000 | API 网关 |

## 四、快速开始

### 4.1 前置依赖

```bash
# 必装
- JDK 17
- Maven 3.9+
- Docker / Docker Compose
- MySQL 8.0+
- Redis 7.0+

# 推荐 IDE
- IntelliJ IDEA Ultimate
```

### 4.2 启动基础设施

```bash
cd deploy
docker-compose up -d mysql redis nacos rocketmq elasticsearch
```

### 4.3 初始化数据库

```bash
mysql -uroot -p < ../docs/08-技术交付物/db/01-schema.sql
mysql -uroot -p < ../docs/08-技术交付物/db/02-initial-data.sql
```

### 4.4 编译构建

```bash
cd backend
mvn clean install -DskipTests
```

### 4.5 启动服务（按顺序）

```bash
# 1. 网关
cd huodaizi-gateway
mvn spring-boot:run

# 2. 用户服务
cd huodaizi-user-service
mvn spring-boot:run

# 3. 会话服务
cd huodaizi-session-service
mvn spring-boot:run

# ... 其他服务类似
```

### 4.6 访问

```
API 文档：http://localhost:8000/doc.html
网关：http://localhost:8000
Nacos：http://localhost:8848/nacos
```

## 五、本骨架的覆盖范围

**已完整实现**（可直接运行）：

- ✅ 父项目 + 共享依赖管理
- ✅ huodaizi-common 完整代码
- ✅ huodaizi-domain 完整代码
- ✅ huodaizi-user-service 完整代码（含 Controller/Service/Repository/Mapper）
- ✅ huodaizi-session-service 完整代码（含 AI 识变逻辑）
- ✅ huodaizi-dispatch-service 完整代码（含三级池算法）
- ✅ Docker Compose 部署
- ✅ K8s 部署模板

**给出框架**（需团队补全）：

- 🔧 list-service / quote-service / credit-service 等其他服务
- 🔧 完整测试用例
- 🔧 CI/CD 配置

## 六、开发规范

### 6.1 包结构

```
com.huodaizi.[module]
  ├── config/        # 配置
  ├── controller/    # 控制器
  ├── service/       # 业务接口
  │   └── impl/      # 业务实现
  ├── repository/    # 数据访问
  ├── entity/        # 实体
  ├── dto/           # 数据传输
  │   ├── request/   # 请求 DTO
  │   └── response/  # 响应 DTO
  ├── mapper/        # 对象转换（MapStruct）
  ├── enums/         # 枚举
  ├── exception/     # 自定义异常
  └── util/          # 工具类
```

### 6.2 命名规范

```
Controller：XxxController
Service Interface：XxxService
Service Impl：XxxServiceImpl
Repository：XxxRepository / XxxMapper
DTO Request：XxxRequest / CreateXxxRequest
DTO Response：XxxResponse / XxxDTO
Entity：Xxx
Enum：XxxEnum
```

### 6.3 API 路径

```
统一前缀：/api/v1

模块前缀：
  /api/v1/users/*
  /api/v1/companies/*
  /api/v1/sessions/*
  /api/v1/lists/*
  /api/v1/quotes/*
```

### 6.4 响应格式

所有 API 统一返回 `Result<T>`：

```json
{
  "code": "0",
  "message": "success",
  "data": { ... },
  "requestId": "req_abc123",
  "timestamp": 1716345600000
}
```

## 七、关键设计

### 7.1 多模块 Maven 管理

父 pom 定义：
- 所有依赖版本
- 所有公共依赖
- 子模块继承

子模块只声明业务依赖。

### 7.2 配置管理（Nacos）

```
应用启动时从 Nacos 拉取配置：
  - application.yml（基础）
  - application-${env}.yml（环境）
  - 业务配置（动态可调）
```

### 7.3 服务间调用

使用 OpenFeign：

```java
@FeignClient(name = "user-service")
public interface UserClient {
    @GetMapping("/api/v1/users/{id}")
    Result<UserDTO> getUser(@PathVariable String id);
}
```

### 7.4 鉴权

使用 Sa-Token：

```java
@SaCheckLogin
@PostMapping("/api/v1/sessions")
public Result<SessionDTO> createSession(@RequestBody CreateSessionRequest request) {
    // ...
}
```

### 7.5 异常处理

全局异常处理器：

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusiness(BusinessException ex) {
        return Result.fail(ex.getCode(), ex.getMessage());
    }
}
```

## 八、性能目标

| 接口 | P95 | 注释 |
|---|---|---|
| 登录 | < 500ms | |
| 创建会话 | < 500ms | |
| AI 识变 | < 3s | 外部 LLM |
| 派单 | < 1s | 含推送 |
| 聚合视图 | < 1s | 含数据库 + Redis |

## 九、监控

- Spring Boot Actuator
- Prometheus + Grafana
- ELK Stack
- SkyWalking（链路追踪）

## 十、配套文档

- API 规范：`docs/08-技术交付物/api/openapi.yaml`
- 数据库 DDL：`docs/08-技术交付物/db/01-schema.sql`
- PRD：`docs/07-产品PRD-v2/`
- 部署运维：`docs/08-技术交付物/ops/`

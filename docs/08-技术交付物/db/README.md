# 数据库 DDL

## 文件

- `01-schema.sql` — 完整建表语句（33 张表，覆盖 11 模块）
- `02-initial-data.sql` — 初始数据（风控规则、市场参考价、测试用户）

## 使用方式

### 本地开发

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE huodaizi CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# 导入 Schema
mysql -u root -p huodaizi < 01-schema.sql

# 导入初始数据
mysql -u root -p huodaizi < 02-initial-data.sql

# 验证
mysql -u root -p huodaizi -e "SHOW TABLES;"
```

### 生产环境

不要直接执行 SQL，必须通过 **数据库迁移工具**（如 Flyway、Liquibase）：

```bash
# Flyway 示例
flyway -url=jdbc:mysql://prod-db:3306/huodaizi \
       -user=*** -password=*** \
       migrate
```

## 表清单（33 张）

### M1 用户与认证（4）

- `users` 用户
- `companies` 企业
- `user_company_mappings` 用户-企业关系
- `growth_accounts` 个人成长账户

### M2 采购会话（5）

- `purchase_sessions` 采购会话
- `demand_cards` 动态需求卡片（版本化）
- `seller_participations` 卖家参与
- `conversation_streams` 对话流
- `messages` 消息
- `ai_intents` AI 识变
- `session_events` 会话时间线

### M3 清单采购（5）

- `procurement_lists` 采购清单
- `procurement_list_lines` 清单明细行
- `list_responses` 卖家清单应答
- `line_quotes` 清单逐行报价
- `optimal_combos` 最优组合方案
- `projects` 项目档案

### M4 报价系统（4）

- `quotes` 报价
- `buyer_selections` 买家选择
- `negotiations` 议价
- `quote_templates` 报价模板

### M5 智能匹配（4）

- `dispatches` 派单记录
- `seller_preferences` 卖家偏好
- `buyer_pool_assignments` 买家池分配
- `market_references` 市场参考价

### M6 信用体系（7）

- `credit_scores` 信用分
- `credit_score_adjustments` 信用分变更
- `seller_verifications` 卖家核验
- `video_showcases` 视频展示
- `reviews` 评价
- `appeals` 申诉
- `blacklists` 黑名单

### M7 卖家工具包（4）

- `seller_customers` 私域 CRM
- `follow_up_tasks` 跟进任务
- `invitation_codes` 邀请码
- `invitation_records` 邀请记录

### M8 买家工具包（3）

- `market_data_subscriptions` 行情订阅
- `buyer_suppliers` 我的供应商
- `comparison_reports` 比价单导出

### M9 微信集成（2）

- `wechat_bindings` 微信绑定
- `virtual_number_calls` 虚拟号通话

### M10 商业化（5）

- `memberships` 会员
- `traffic_wallets` 流量账户
- `traffic_charges` 流量扣费
- `saas_contracts` SaaS 合同
- `data_subscriptions` 数据订阅

### M11 风控（4）

- `risk_rules` 风控规则
- `risk_events` 风控事件
- `region_alerts` 区域预警
- `device_fingerprints` 设备指纹

### 辅助（1）

- `audit_logs` 审计日志

## 设计原则

### 1. 主键
- 业务实体用 VARCHAR(32) 业务 ID（如 `ps_xxxxxx`）
- 日志类用 BIGINT AUTO_INCREMENT

### 2. 时间字段
- `created_at` 创建时间（必有）
- `updated_at` 更新时间（业务表必有）
- 使用 DATETIME 而非 TIMESTAMP（避免 2038 问题）

### 3. 字符集
- 全表 `utf8mb4_0900_ai_ci`（支持 emoji + 大小写不敏感）

### 4. JSON 字段
- 多变属性用 JSON 字段（如 `add_ons`、`tier_pricing`）
- 不需要查询的元数据用 JSON

### 5. 索引策略
- 高频查询字段建立联合索引
- 软删除字段索引
- 时间范围查询建索引

### 6. 软删除
- 关键业务数据不物理删除
- 用 `status = 'cancelled'` 等枚举标识
- 用户企业关系用 `removed_at` 标记

### 7. 分库分表预留
- 大表（`messages`、`session_events`、`risk_events`、`audit_logs`）按用户 ID hash 分库
- M12+ 启动分库分表

## 性能优化建议

| 表 | 数据量预估（M12） | 建议 |
|---|---|---|
| messages | 千万级 | 按月分区，冷数据归档 |
| session_events | 千万级 | 按月分区 |
| risk_events | 千万级 | 按月分区 |
| dispatches | 百万级 | 按 seller_id hash 分表 |
| quotes | 百万级 | 按 session_id hash 分表 |
| audit_logs | 千万级 | 按月分区 + 6 个月归档到对象存储 |

## 备份与恢复

```bash
# 每日全量备份（推荐 1:00 AM）
mysqldump -u backup --single-transaction --quick \
  --routines --triggers --events \
  huodaizi | gzip > /backup/huodaizi_$(date +%Y%m%d).sql.gz

# 每小时 binlog 备份
mysqlbinlog ... > /backup/binlog/

# 恢复
zcat /backup/huodaizi_20260523.sql.gz | mysql -u root -p huodaizi
mysqlbinlog binlog.000001 | mysql -u root -p huodaizi
```

## 监控指标

- 慢 SQL（>100ms）
- 锁等待
- 连接池利用率
- 主从延迟（< 1s）
- 磁盘使用率（< 75%）

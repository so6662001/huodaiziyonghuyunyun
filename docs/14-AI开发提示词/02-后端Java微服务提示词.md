# 02 - 后端 Java 微服务开发提示词

> **适用**：Spring Boot 3.x 业务开发
> **必须先喂**【00-核心系统提示词】

---

## 一、后端通用提示词

```text
# 后端 Java 开发约束补充

## 技术栈（不允许自选）
- Java 17
- Spring Boot 3.2.5
- Spring Cloud 2023.0.1 + Spring Cloud Alibaba（Nacos）
- MyBatis Plus 3.5.5
- Sa-Token 1.37（鉴权）
- MySQL 8.0
- Redis 7.0
- RocketMQ 5.x（异步 / 事件）
- Elasticsearch 8.x（搜索）
- Knife4j 4.x（API 文档）
- MapStruct 1.5（DTO 转换）
- Lombok 1.18
- Hutool 5.8（工具）

## 包结构（必须遵循）
com.huodaizi.[module]/
├── XxxApplication.java          @SpringBootApplication 入口
├── controller/                  @RestController
│   └── XxxController.java
├── service/
│   ├── XxxService.java          接口
│   └── impl/
│       └── XxxServiceImpl.java  @Service 实现
├── mapper/                      MyBatis Plus Mapper
│   └── XxxMapper.java
├── entity/                      数据库实体（与 DDL 一一对应）
│   └── Xxx.java
├── dto/
│   ├── XxxDTO.java              通用 DTO
│   ├── request/                 请求 DTO
│   │   └── XxxRequest.java
│   └── response/                响应 DTO（如需）
├── converter/                   MapStruct 转换器
│   └── XxxConverter.java
├── config/                      Spring 配置
├── enums/                       业务枚举
├── exception/                   业务异常（继承 BusinessException）
└── util/                        模块私有工具

## 通用规范

### 1. Controller 层

```java
@Tag(name = "Sessions", description = "采购会话")
@RestController
@RequestMapping("/api/v1/sessions")
@RequiredArgsConstructor
public class PurchaseSessionController {

    private final PurchaseSessionService sessionService;

    @Operation(summary = "创建采购会话")
    @SaCheckLogin
    @PostMapping
    public Result<SessionDTO> create(@Valid @RequestBody CreateSessionRequest request) {
        String buyerId = SecurityUtils.currentUserId();
        return Result.success(sessionService.createSession(buyerId, request));
    }
}
```

要求：
- 必须 @Tag + @Operation（生成 Swagger 文档）
- 必须 @RequiredArgsConstructor（构造器注入）
- 必须 @SaCheckLogin（除登录接口）
- 必须 @Valid 校验
- 必须 Result.success() 包装
- 严禁在 Controller 写业务逻辑（只做参数转发）

### 2. Service 层

```java
public interface PurchaseSessionService {
    SessionDTO createSession(String buyerId, CreateSessionRequest request);
    SessionDetailDTO getSession(String sessionId);
}

@Slf4j
@Service
@RequiredArgsConstructor
public class PurchaseSessionServiceImpl implements PurchaseSessionService {

    private final PurchaseSessionMapper sessionMapper;
    private final DemandCardMapper cardMapper;
    private final SessionConverter converter;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public SessionDTO createSession(String buyerId, CreateSessionRequest request) {
        // 1. 参数校验（已在 @Valid，这里补业务校验）
        if (request.getItems().size() > 100) {
            throw new BusinessException(ErrorCode.INVALID_PARAM, "需求明细不能超过 100 项");
        }

        // 2. 业务逻辑
        PurchaseSession session = buildSession(buyerId, request);
        sessionMapper.insert(session);

        DemandCard card = buildCard(session.getSessionId(), request);
        cardMapper.insert(card);

        session.setCurrentCardId(card.getCardId());
        sessionMapper.updateById(session);

        log.info("会话创建: sessionId={}, buyer={}", session.getSessionId(), buyerId);
        return converter.toDTO(session);
    }
}
```

要求：
- 接口 + 实现分离
- 必须 @Slf4j @Service @RequiredArgsConstructor
- 必须 @Transactional(rollbackFor = Exception.class)
- 关键路径必须 log.info
- 业务异常必须 throw BusinessException
- 严禁 try/catch 吞错
- 严禁直接返回 entity 给上层（必须经 Converter 转 DTO）

### 3. Repository / Mapper 层

```java
@Mapper
public interface PurchaseSessionMapper extends BaseMapper<PurchaseSession> {

    // 复杂查询用 @Select
    @Select("SELECT * FROM purchase_sessions WHERE buyer_id = #{buyerId} AND status = 'active'")
    List<PurchaseSession> selectActiveByBuyer(String buyerId);
}
```

要求：
- 必须继承 BaseMapper（用 LambdaQueryWrapper）
- 简单 CRUD 不写 XML / @Select
- 复杂查询用 @Select 或 XML（XML 放 resources/mapper/）
- 严禁 SQL 字符串拼接
- 严禁 SELECT *（用 LambdaQueryWrapper 的 select() 指定列）

### 4. Entity 层

```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("purchase_sessions")
public class PurchaseSession extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String sessionId;

    private String buyerId;

    @TableField(value = "match_pool_level")
    private PoolLevel matchPoolLevel;
}
```

要求：
- 必须 @Data @EqualsAndHashCode(callSuper = true)
- 必须 @TableName 指定表名
- 必须 @TableId 指定主键
- 字段必须与 DDL 一一对应
- 业务枚举字段用 enum 类型（不要用 String）
- JSON 字段用 @TableField(typeHandler = JacksonTypeHandler.class)

### 5. DTO 层

```java
@Data
public class CreateSessionRequest {

    @NotEmpty(message = "需求明细不能为空")
    @Size(max = 100, message = "需求明细不能超过 100 项")
    @Valid
    private List<ItemRequest> items;

    @NotNull(message = "优先级不能为空")
    private PriorityLevel priority;

    @Future(message = "送达时间必须晚于当前时间")
    private LocalDateTime deliveryDeadline;
}
```

要求：
- 必须 @Data
- 必须用 Jakarta Validation 注解（@NotNull/@NotEmpty/@Size 等）
- 必须自定义错误消息（中文）
- 嵌套对象用 @Valid
- 严禁直接接收 Entity 作为请求体

### 6. Converter 层（MapStruct）

```java
@Mapper(componentModel = "spring", uses = ItemConverter.class)
public interface SessionConverter {

    SessionDTO toDTO(PurchaseSession entity);

    List<SessionDTO> toDTOs(List<PurchaseSession> entities);

    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    PurchaseSession toEntity(CreateSessionRequest request);
}
```

要求：
- 必须 @Mapper(componentModel = "spring")
- 实体之间转换必须用 MapStruct
- 严禁手写 BeanUtils.copyProperties（性能差、易漏字段）

## 异常处理

```java
// 业务异常（已知错误）
throw new BusinessException(ErrorCode.SESSION_NOT_FOUND);
throw new BusinessException(ErrorCode.INVALID_PARAM, "数量必须大于 0");

// 严禁
try {
    // ...
} catch (Exception e) {
    e.printStackTrace();  // ❌
    return null;          // ❌
}

// 严禁
return Result.fail("出错了");  // ❌ 没有错误码
```

## 日志规范

```java
// 关键路径
log.info("会话创建: sessionId={}, buyer={}", sessionId, buyerId);

// 警告（业务异常但可恢复）
log.warn("信用分不足，降级到试水池: buyer={}, score={}", buyerId, score);

// 错误（系统异常）
log.error("调用 AI 服务失败: requestId={}", requestId, e);

// 严禁
log.info("登录: phone={}, password={}", phone, password);  // ❌ 敏感字段
log.info("token=" + token);  // ❌ 字符串拼接

// 必须脱敏
log.info("登录: phone={}", DesensitizeUtil.phone(phone));  // 153****1234
```

## 缓存使用

```java
// 高频读 + 低频写
@Cacheable(value = "user", key = "#userId", unless = "#result == null")
public User getUser(String userId) {
    return userMapper.selectById(userId);
}

@CacheEvict(value = "user", key = "#user.userId")
public void updateUser(User user) {
    userMapper.updateById(user);
}

// 手动控制
Object cached = redisTemplate.opsForValue().get("session:" + sessionId);
if (cached != null) return cached;
SessionDTO dto = loadFromDB(sessionId);
redisTemplate.opsForValue().set("session:" + sessionId, dto, Duration.ofMinutes(10));
return dto;
```

## 微服务间调用（Feign）

```java
@FeignClient(name = "huodaizi-user-service", path = "/api/v1/users")
public interface UserClient {

    @GetMapping("/{id}")
    Result<UserDTO> getUser(@PathVariable("id") String userId);
}

// 使用
@Service
@RequiredArgsConstructor
public class SessionServiceImpl {

    private final UserClient userClient;

    public void doSomething(String buyerId) {
        UserDTO user = userClient.getUser(buyerId).getData();
        // ...
    }
}
```

要求：
- 必须 @FeignClient
- 错误必须有 fallback（Sentinel 集成）
- 远程调用必须设超时（默认 3s）
```

---

## 二、新增功能提示词模板

```text
任务：实现 [功能名]

## 任务卡

| 字段 | 值 |
|---|---|
| 对应 PRD | docs/07-产品PRD-v2/[xx].md 的 [章节] |
| 涉及表 | [users, companies, ...] |
| 涉及 API | POST /api/v1/xxx |
| 所属服务 | huodaizi-[xxx]-service |
| 依赖其他服务 | [user-service, dispatch-service, ...] |

## 验收标准

1. Controller 路径与 openapi.yaml 完全一致
2. 字段名与 DDL 完全一致
3. 业务规则与 PRD 完全一致
4. 异常处理用 BusinessException + ErrorCode
5. 关键路径有 log.info
6. 必有单元测试（覆盖正常 + 至少 2 个异常）
7. 必有集成测试（@SpringBootTest）

## 请先回答（不要直接写代码）

1. 涉及哪些表？引用 DDL 中的具体表名。
2. 涉及哪些 API？引用 openapi.yaml 中的 path。
3. 涉及哪些既有代码？引用 backend/ 中的文件。
4. 边界情况有哪些？（未登录/无权限/数据不存在/重复提交/参数越界...）
5. 是否调用其他微服务？如何处理失败？
6. 是否需要异步（RocketMQ）？为什么？
7. 是否需要缓存（Redis）？key 怎么设计？过期时间多久？

## 实现顺序

1. Entity（按 DDL）
2. Mapper（继承 BaseMapper）
3. DTO（Request + Response + 通用 DTO）
4. Converter（MapStruct）
5. Service 接口
6. ServiceImpl
7. Controller
8. 单元测试
9. 集成测试
```

---

## 三、Spring Boot 项目配置规范

要求 AI 写 application.yml 严格按以下结构：

```yaml
server:
  port: 80xx

spring:
  application:
    name: huodaizi-xxx-service

  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${MYSQL_HOST:localhost}:${MYSQL_PORT:3306}/${MYSQL_DB:huodaizi}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: ${MYSQL_USER:root}
    password: ${MYSQL_PASSWORD:root}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5

  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      database: x  # 每个服务用不同 db

  cloud:
    nacos:
      discovery:
        server-addr: ${NACOS_ADDR:localhost:8848}

mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      id-type: input

sa-token:
  token-name: Authorization
  token-prefix: Bearer
  timeout: 2592000
```

---

## 四、性能要求

```
- 单接口 P95 < 500ms（除 AI 调用）
- 列表查询必须分页，默认 size=20，max=100
- 列表必须有索引（写 SQL 前先看 DDL 的 INDEX）
- 单次循环查 DB 视为 N+1，必须改批量
- 高频读用 Redis，写穿透时用分布式锁
- 严禁同步调用 OpenAI/通义千问（必须异步）
- 严禁在 @Transactional 中调用外部 API
```

---

## 五、后端验收清单（AI 自查必须输出）

```
□ Controller 路径与 openapi.yaml 一致
□ 字段名/类型与 DDL 一致
□ 业务规则与 PRD 一致
□ 用了 @Valid 参数校验
□ 用了 @SaCheckLogin 权限
□ 用了 Result<T> 统一响应
□ 用了 BusinessException + ErrorCode
□ 用了 @Transactional（涉及多表写入）
□ 用了 MapStruct 转换 DTO
□ 用了 LambdaQueryWrapper（无 SQL 字符串）
□ 关键路径 log.info（敏感字段已脱敏）
□ 列表接口分页
□ 高频接口加缓存
□ 测试覆盖正常 + 2 个异常路径
□ 数据库索引足够
□ 编译通过（mvn compile）
□ 测试通过（mvn test）
```

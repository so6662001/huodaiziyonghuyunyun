# 04 - API 开发提示词（严格按 OpenAPI）

> **用途**：确保 AI 实现的 API **路径、请求体、响应体与 OpenAPI 规范完全一致**。

---

## 一、API 开发通用提示词

```text
# API 实现约束

## 强制规则

### 1. API 契约不可改

所有 API 的【path、method、request body、response body、错误码】
都必须能在 docs/08-技术交付物/api/openapi.yaml 中找到。

如果你认为现有 API 设计不合理，必须：
  1. 先停止编码
  2. 在 PR 中说明建议
  3. 等产品/架构师确认后才能修改 openapi.yaml
  4. 改完 yaml 再写代码

严禁：擅自加字段、删字段、改类型、改路径。

### 2. 字段命名 camelCase（不是 snake_case）

```json
// ✅ 正确
{
  "sessionId": "ps_240523001234",
  "buyerId": "u_240523123",
  "currentCardId": "card_240523456"
}

// ❌ 错误
{
  "session_id": "...",
  "buyer-id": "...",
  "CurrentCardId": "..."  // 大驼峰
}
```

### 3. 响应格式必须用 Result<T>

```json
{
  "code": "0",
  "message": "success",
  "data": { ... },
  "requestId": "req_xxx",
  "timestamp": 1716345600000
}
```

错误响应：

```json
{
  "code": "11001",
  "message": "会话不存在",
  "data": null,
  "details": { ... },  // 可选
  "requestId": "req_xxx",
  "timestamp": 1716345600000
}
```

### 4. 错误码规范

参考 com.huodaizi.common.api.ErrorCode（已定义）

- 0：成功
- 1001-1099：通用错误
- 10101-10199：用户模块
- 10201-10299：企业模块
- 11001-11099：会话模块
- 12001-12099：报价模块
- 13001-13099：清单模块
- 14001-14099：派单模块
- 15001-15099：信用模块
- 16001-16099：商业化模块
- 17001-17099：风控模块

新增错误码必须：
  1. 加到 ErrorCode 枚举
  2. 加到 openapi.yaml 的 error_codes 段
  3. 加到错误码文档（docs/08-技术交付物/api/error-codes.md）

### 5. 分页规范

请求：
```
GET /api/v1/xxx?pageToken=xxx&pageSize=20
```

响应：
```json
{
  "code": "0",
  "data": {
    "items": [ ... ],
    "pagination": {
      "pageSize": 20,
      "total": 156,
      "nextPageToken": "eyJpZCI6MTAwfQ==",
      "hasMore": true
    }
  }
}
```

要求：
- pageSize 默认 20，最大 100
- 使用 cursor-based 分页（不是 offset）
- 必须返回 total（用于显示总数）
- 必须返回 hasMore（用于无限滚动）

### 6. 时间格式

- 时间字段统一 ISO 8601：`2026-05-23T10:30:00+08:00`
- 时间戳字段 Long 类型（毫秒）：`1716345600000`
- 接收时间用 `LocalDateTime`（Java）
- 严禁 yyyy/MM/dd HH:mm:ss 字符串格式

### 7. 金额字段

- 金额用 `BigDecimal`（Java），不用 double
- JSON 中用数字，保留 2 位小数：`3950.00`
- 严禁单位混用（统一"元/吨"）

### 8. 枚举字段

- JSON 中传字符串枚举：`"status": "active"`
- 严禁传 number 枚举（前端难维护）
- 枚举值用 snake_case：`session_closed` 不是 `sessionClosed`

### 9. 必填 vs 可选

- 必填字段：用 @NotNull / @NotBlank
- 可选字段：JSON 中可以不传或 null
- 严禁用 `""`（空字符串）表示 null
- 严禁用 `0` 表示无值（数字字段用 null）

### 10. 接口幂等

- POST 创建类接口必须支持 clientTempId（客户端临时 ID）
- 相同 clientTempId 在 5 分钟内重复请求返回相同结果
- PUT/PATCH 必须幂等（多次调用结果一致）
- DELETE 必须幂等（不存在也返回成功）

## 必须实现的元能力

### Idempotency-Key 幂等键

```java
@PostMapping
public Result<XxxDTO> create(
        @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey,
        @RequestBody CreateRequest request) {
    // 1. 校验 idempotencyKey 是否已处理
    // 2. 如已处理，返回缓存结果
    // 3. 如未处理，执行业务 + 缓存结果
}
```

### Rate Limit 频率限制

```java
@RateLimit(key = "#userId", count = 100, period = 60) // 每分钟 100 次
@PostMapping
public Result<XxxDTO> xxx(...) { ... }
```

### 链路追踪

- 必须从 Header 读取 X-Request-Id（无则生成）
- 必须放入 MDC：MDC.put("requestId", requestId)
- 必须在响应 Header 中返回 X-Request-Id
- 必须在日志中输出 requestId

参考 huodaizi-common 的 RequestIdFilter（已实现）

## API 测试规范

每个 API 必须有以下测试：

1. 正常路径（happy path）
2. 参数校验失败（@Valid 各项规则）
3. 业务异常（数据不存在 / 权限不足 / 业务规则违反）
4. 系统异常模拟（DB 断 / Redis 断）
5. 幂等性（同 idempotencyKey 重复调用）
6. 边界（最大值 / 最小值 / 空数组 / 长字符串）
```

---

## 二、新增 API 提示词模板

```text
任务：实现 API [METHOD] [path]

## 任务卡

| 字段 | 值 |
|---|---|
| openapi.yaml 编号 | （行号或锚点） |
| 所属服务 | huodaizi-xxx-service |
| 权限要求 | @SaCheckLogin / 自定义 |
| 涉及表 | xxx, yyy |
| 涉及其他服务 | （如有） |

## 请先输出（不要直接写代码）

### 1. 从 openapi.yaml 摘录契约

```yaml
/api/v1/xxx:
  post:
    summary: ...
    requestBody:
      content:
        application/json:
          schema: ...
    responses:
      "200":
        ...
```

### 2. 列出涉及的字段

| 字段 | 来源（DDL 表名.列名） | 类型 | 必填 | 校验规则 |
|---|---|---|---|---|
| sessionId | purchase_sessions.session_id | String | Y | 长度 ≤ 32 |
| ... | | | | |

### 3. 列出业务规则

引用 PRD 段落：
- "会话创建时，priority 默认 standard"（来源：docs/07-产品PRD-v2/02-采购会话核心模块.md 第 X 节）
- "deliveryDeadline 必须晚于 now + 1h"（同上）
- ......

### 4. 列出错误码

| 场景 | 错误码 | 消息 |
|---|---|---|
| 用户未登录 | 1003 | UNAUTHORIZED |
| 表单校验失败 | 1002 | INVALID_PARAM |
| 数量超限 | 11005 | CHANGE_LIMIT_EXCEEDED |
| ......  | | |

### 5. 列出测试用例

- 正常：xxx
- 异常 1：xxx
- 异常 2：xxx
- 异常 3：xxx
- 边界 1：xxx
- 边界 2：xxx

## 实现

按上面的契约 + 规则 + 错误码实现。

## 自查

□ path / method / req / resp 与 openapi.yaml 一致
□ 字段名 camelCase
□ 用了 Result<T>
□ 用了 BusinessException + ErrorCode
□ 用了 @Valid 校验
□ 用了 @SaCheckLogin 权限
□ 有 @Operation @Tag 文档注解
□ 关键路径有 log.info
□ 敏感字段已脱敏
□ 有单元 + 集成测试
□ 测试通过（mvn test）
□ Swagger 文档生成正常
```

---

## 三、修改 API 提示词

```text
任务：修改 API [METHOD] [path]

## 警告

修改 API 是高风险操作。在修改前必须回答：

1. 改字段：是新增、删除、还是改名/改类型？
2. 兼容性：现有调用方是否会受影响？
3. 端：买家小程序 / 卖家小程序 / 后台 / 第三方？
4. 版本：是 v1 → v1.1（兼容）还是 v1 → v2（不兼容）？

## 字段变更规则

| 变更 | 是否兼容 | 处理 |
|---|---|---|
| 新增可选字段 | ✅ 兼容 | 直接改 |
| 新增必填字段 | ❌ 不兼容 | 升 v2，或给默认值变可选 |
| 删除字段 | ❌ 不兼容 | 升 v2，或保留字段但 deprecated |
| 改字段类型 | ❌ 不兼容 | 升 v2 |
| 改字段名 | ❌ 不兼容 | 升 v2，或同时支持新旧名 |
| 改 path | ❌ 不兼容 | 升 v2，旧 path 保留 redirect |

## 改动顺序

1. 改 openapi.yaml（先有契约后有代码）
2. 通知所有调用方（前端、其他服务）
3. 改后端实现
4. 改测试
5. 改 SDK / 文档
6. PR 标题加 [API-BREAKING] 或 [API-COMPAT]
```

---

## 四、API 版本管理

```text
版本演进规则：

v1 → v1.1（向后兼容）
  - 加可选字段
  - 加新接口
  - 改响应非破坏性字段
  → 不需要改路径

v1 → v2（不兼容）
  - 删字段 / 改名 / 改类型 / 必填字段
  → 路径改为 /api/v2/xxx
  → v1 保留至少 6 个月
  → 在 v1 响应 Header 加 Deprecation: true

强制流程：

1. 写 RFC（在 docs/15-API变更/RFC-XXX.md）
2. 团队评审
3. 改 openapi.yaml
4. 实现 v2
5. 通知所有调用方
6. 6 个月后下线 v1
```

---

## 五、AI 常翻车的 API 问题

```
❌ 翻车 1：字段名错乱
  AI 写：sessionId
  实际 OpenAPI：session_id
  解决：开发前必须粘贴 OpenAPI 片段

❌ 翻车 2：错误码自创
  AI 写：return Result.fail("error", "会话不存在")
  应该：return Result.fail(ErrorCode.SESSION_NOT_FOUND)
  解决：强制 ErrorCode 枚举

❌ 翻车 3：返回类型不一致
  AI 写：return Result.success(entity)
  应该：return Result.success(converter.toDTO(entity))
  解决：强制 DTO 转换

❌ 翻车 4：忘了分页
  AI 写：List<XxxDTO> list
  应该：PageResult<XxxDTO>
  解决：列表必须分页

❌ 翻车 5：时间格式错乱
  AI 写：String createdAt = "2026/05/23"
  应该：LocalDateTime createdAt（ISO 8601）

❌ 翻车 6：金额用 double
  AI 写：double price
  应该：BigDecimal price
  解决：金额绝对禁止 double（精度问题）

❌ 翻车 7：权限漏加
  AI 写：@PostMapping public Result xxx
  应该：@SaCheckLogin @PostMapping public Result xxx
  解决：除登录接口外所有接口必须 @SaCheckLogin

❌ 翻车 8：日志泄漏敏感字段
  AI 写：log.info("登录请求: {}", request)（request 包含密码）
  应该：log.info("登录请求: phone={}", desensitizePhone(request.getPhone()))
```

---

## 六、API 测试模板

要求 AI 必须提供以下测试：

```java
@SpringBootTest
@AutoConfigureMockMvc
class SessionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PurchaseSessionService sessionService;

    @Test
    @DisplayName("创建会话 - 正常")
    void createSession_normal() throws Exception {
        // given
        CreateSessionRequest request = buildRequest();
        when(sessionService.createSession(any(), any()))
                .thenReturn(buildResponse());

        // when & then
        mockMvc.perform(post("/api/v1/sessions")
                .contentType(APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request))
                .header("Authorization", "Bearer mock-token"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value("0"))
                .andExpect(jsonPath("$.data.sessionId").exists());
    }

    @Test
    @DisplayName("创建会话 - 未登录")
    void createSession_unauthorized() throws Exception {
        mockMvc.perform(post("/api/v1/sessions")
                .contentType(APPLICATION_JSON)
                .content("{}"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("创建会话 - 参数为空")
    void createSession_emptyItems() throws Exception {
        CreateSessionRequest request = new CreateSessionRequest();
        request.setItems(Collections.emptyList());

        mockMvc.perform(post("/api/v1/sessions")
                .contentType(APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request))
                .header("Authorization", "Bearer mock-token"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("1002"));
    }
}
```

要求：
- 每个接口至少 3 个测试（正常 + 2 个异常）
- 必须 @DisplayName 注释场景
- 必须断言关键字段
- 必须用 MockMvc（不要直接 new Controller）

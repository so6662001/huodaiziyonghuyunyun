# API 规范文档

## 文件

- `openapi.yaml` — OpenAPI 3.0 完整 API 规范

## 使用方式

### 1. 在 Swagger UI 中预览

```bash
# 方式 A: Docker
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v $(pwd):/spec swaggerapi/swagger-ui

# 方式 B: 在线
# 把 openapi.yaml 内容粘贴到 https://editor.swagger.io
```

### 2. 生成客户端 SDK

```bash
# TypeScript
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml -g typescript-axios -o ./sdk-ts

# Java
openapi-generator-cli generate \
  -i openapi.yaml -g java -o ./sdk-java

# Go
openapi-generator-cli generate \
  -i openapi.yaml -g go -o ./sdk-go
```

### 3. 生成 Mock Server

```bash
npm install -g @stoplight/prism-cli
prism mock openapi.yaml
# 默认 http://127.0.0.1:4010
```

### 4. 接入 Postman

直接 `Import → Link/File` 选择 `openapi.yaml`，自动生成 Collection。

## API 覆盖范围

| 模块 | 端点数 | 状态 |
|---|---|---|
| M1 用户与认证 | 8 | ✅ |
| M2 采购会话 | 12 | ✅ |
| M3 清单采购 | 10 | ✅ |
| M4 报价系统 | 11 | ✅ |
| M5 智能匹配 | 5 | ✅ |
| M6 信用体系 | 5 | ✅ |
| M9 微信集成 | 3 | ✅ |
| M10 商业化 | 7 | ✅ |
| M11 风控 | 2 | ✅ |
| **合计** | **63** | |

## 通用约定

- 所有时间：ISO 8601 UTC（`2026-05-23T14:32:00Z`）
- 金额：元，保留 2 位小数
- 重量：吨，保留 3 位小数
- 鉴权：Bearer Token (JWT)
- 错误响应格式：

```json
{
  "code": "INVALID_PARAM",
  "message": "数量必须大于 0",
  "details": { "field": "quantity_ton" },
  "request_id": "req_abc123"
}
```

## 鉴权流程

```
1. 客户端调用 /auth/wechat-login 或 /auth/sms-login
2. 服务端返回 { access_token, refresh_token, expires_in }
3. 客户端在后续请求头携带：Authorization: Bearer {access_token}
4. access_token 过期前调用 /auth/refresh 续期
```

## 版本管理

- URL 版本：`/v1`, `/v2`
- 不向下兼容的变更必须升版本号
- 旧版本至少维护 6 个月

## 灰度发布

通过 HTTP Header `X-Release-Channel: stable | canary | beta` 控制流量分配。

# huodaizi-risk-service 风控服务

## 职责
- 36 条反作弊规则引擎
- 设备指纹、IP 风控
- 事件流式检测（Flink）
- 围猎检测（图算法）
- 规则配置中心

## 核心 API

```
POST   /api/v1/risk/check                       同步风控检查
POST   /api/v1/risk/events                      上报事件
GET    /api/v1/risk/rules                       规则列表（admin）
PATCH  /api/v1/risk/rules/{id}                  调整规则
```

## 状态
🔧 骨架待补全

详见 `docs/03-扩展交付物/03-3-反作弊规则引擎.md`

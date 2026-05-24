# huodaizi-credit-service 信用服务

## 职责
- 买家/卖家信用分实时计算
- 评价管理（双向匿名）
- 申诉处理（48h 闭环）
- 黑名单管理

## 核心 API

```
GET    /api/v1/credits/me                       当前用户信用
GET    /api/v1/credits/users/{id}/score         查询用户信用
GET    /api/v1/credits/users/{id}/history       信用历史

POST   /api/v1/credits/reviews                  发表评价
GET    /api/v1/credits/reviews                  评价列表

POST   /api/v1/appeals                          发起申诉
GET    /api/v1/appeals/{id}                     查询申诉
POST   /api/v1/appeals/{id}/respond             申诉响应
```

## 状态
🔧 骨架待补全

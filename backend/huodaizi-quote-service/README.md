# huodaizi-quote-service 报价服务

## 职责
- 卖家报价/还价
- 6 维结构化报价（数量/价格/交期/付款/质量/服务）
- 实时价格计算（基价 + 加项）
- 报价对比、Top1 推荐
- 议价记录与封顶（5 轮）

## 核心 API

```
POST   /api/v1/quotes                创建报价
GET    /api/v1/quotes/{id}           查询报价
PATCH  /api/v1/quotes/{id}           修改报价
POST   /api/v1/quotes/{id}/withdraw  撤回报价

POST   /api/v1/negotiations          发起议价
GET    /api/v1/negotiations/{id}     查询议价
POST   /api/v1/negotiations/{id}/respond  议价响应
```

## 状态
🔧 骨架待补全

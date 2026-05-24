# huodaizi-commercial-service 商业化服务

## 职责
- 会员管理（卖家：免费/银/金/铂金）
- 流量费 / CPM / CPC 计费
- SaaS 订阅
- 钱包 / 充值 / 退款
- 财务结算

## 核心 API

```
GET    /api/v1/memberships/me                   当前会员信息
POST   /api/v1/memberships/upgrade              升级会员

GET    /api/v1/billing/wallet                   钱包余额
POST   /api/v1/billing/recharge                 充值
GET    /api/v1/billing/transactions             流水
POST   /api/v1/billing/refund                   退款申请

POST   /api/v1/ads/campaigns                    流量包采购
GET    /api/v1/ads/campaigns/{id}/stats         投放数据
```

## 状态
🔧 骨架待补全

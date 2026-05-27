# huodaizi-notification-service 通知服务

## 职责
- 短信下发（阿里云/腾讯云）
- 微信公众号模板消息
- 微信小程序订阅消息
- 企业微信机器人消息
- 站内信
- App Push（v2）

## 核心 API

```
POST   /api/v1/notify/sms                       短信
POST   /api/v1/notify/wechat-template           微信模板消息
POST   /api/v1/notify/wework                    企微机器人
POST   /api/v1/notify/in-app                    站内信

GET    /api/v1/notifications                    站内信列表
PATCH  /api/v1/notifications/{id}/read          标记已读
```

## 状态
🔧 骨架待补全

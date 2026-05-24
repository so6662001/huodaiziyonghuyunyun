# huodaizi-list-service 清单服务

## 职责
- 接收 Excel/PDF/图片清单上传
- 调用 ai-service 做 OCR + LLM 解析
- 清单规范化、字段对齐、置信度评估
- 智能拆单（按品种/规格/区域）
- 最优组合算法（多卖家组合报价）

## 状态
🔧 **骨架待补全**。结构同 `huodaizi-user-service`。

## 核心包结构（待开发）

```
com.huodaizi.list/
├── ListApplication.java
├── controller/
│   ├── ListController.java
│   └── ListUploadController.java
├── service/
│   ├── ListService.java
│   ├── ListParseService.java       # 调用 AI 解析
│   ├── ListSplitService.java       # 拆单算法
│   └── OptimalComboService.java    # 最优组合算法
├── entity/
│   ├── PurchaseList.java
│   ├── ListItem.java
│   └── ListSplit.java
└── mapper/
    └── PurchaseListMapper.java
```

## 关键 API

```
POST   /api/v1/lists/upload          上传清单
POST   /api/v1/lists/{id}/parse      触发解析
GET    /api/v1/lists/{id}            查询清单
POST   /api/v1/lists/{id}/confirm    买家确认
POST   /api/v1/lists/{id}/split      拆单建议
POST   /api/v1/lists/{id}/optimal-combo  最优组合
```

详见：`docs/07-产品PRD-v2/03-清单采购模块.md`

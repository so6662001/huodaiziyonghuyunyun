# huodaizi-ai-service AI 服务

## 职责
- OCR：营业执照、清单图片
- LLM：意图识别、清单解析（通义千问/GPT）
- 嵌入向量、相似度计算
- 价格智能预估
- 异常文本检测

## 核心 API

```
POST   /api/v1/ai/ocr/business-license          营业执照 OCR
POST   /api/v1/ai/ocr/list                      清单 OCR

POST   /api/v1/ai/parse/list                    清单 LLM 解析
POST   /api/v1/ai/parse/intent                  消息意图识别
POST   /api/v1/ai/parse/spec                    规格识别

POST   /api/v1/ai/embed                         文本嵌入
POST   /api/v1/ai/predict/price                 价格预估
```

## 集成

- 通义千问 (Aliyun DashScope)
- GPT-4o-mini（备用）
- 阿里云 OCR

## 状态
🔧 骨架待补全

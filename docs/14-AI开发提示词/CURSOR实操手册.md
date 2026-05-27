# Cursor 实操手册（手把手）

> **目的**：让您在 Cursor 中使用这套提示词的每一步都清晰可执行。
> **预设**：您已经安装了 Cursor、克隆了本仓库。

---

## 一、初始化（一次性，5 分钟）

### Step 1：用 Cursor 打开仓库

```bash
# 打开仓库根目录
cd /path/to/huodaiziyonghuyunyun
cursor .
```

### Step 2：确认 .cursorrules 已生效

```
1. 打开 Cursor → Settings (Cmd+,)
2. 搜索 "Rules"
3. 应看到 "Project Rules" 已加载 .cursorrules 文件
4. 如果看不到，重启 Cursor
```

**验证生效**：

在 Cursor 中按 `Cmd+L` 打开 Chat，输入：

```
请回答 5 个问题验证你的角色：
1. 你是什么项目的什么角色？
2. 我们的核心场景是单条规格还是多规格？
3. 后端用什么版本的 Spring Boot？
4. UI 颜色 Token 在哪个文件？
5. 移动端按钮最小高度是多少？
```

**期望回答**：
1. 货袋子（钢贸 B2B）资深全栈工程师
2. 多规格（80%+ 是 5-30 行）
3. Spring Boot 3.2.5 + Java 17
4. `docs/13-Figma设计规范/design-tokens/tokens.json` 或 `styles.css`
5. 关键 CTA ≥ 44pt

✅ **全对**：配置成功
❌ **错 ≥ 2 个**：重启 Cursor 再试

### Step 3：选择 AI 模型

```
推荐：Claude 3.5 Sonnet（最稳定）
备选：Claude 3.7 Sonnet / GPT-4o

设置位置：Cursor → 右下角 → 模型选择
```

### Step 4：熟悉 3 个核心快捷键

```
Cmd + L    打开右侧 Chat（轻量问答）
Cmd + I    打开 Composer（多文件编辑，重型工作）
Cmd + K    内联编辑（在代码中直接修改）
```

---

## 二、日常开发标准流程（每个任务）

### 流程图

```
┌─────────────────────────────────────────┐
│ 1. 确定任务类型 → 选模板                  │
├─────────────────────────────────────────┤
│ 2. 在 Composer 中粘贴模板 + 填任务卡      │
├─────────────────────────────────────────┤
│ 3. AI 输出"设计资产清单" → 人工审核        │
├─────────────────────────────────────────┤
│ 4. AI 实现代码 → 多文件应用                │
├─────────────────────────────────────────┤
│ 5. AI 输出"6 维自检报告" → 核对            │
├─────────────────────────────────────────┤
│ 6. 人工抽查 + 测试                         │
├─────────────────────────────────────────┤
│ 7. 提交 PR                                │
└─────────────────────────────────────────┘
```

### 详细步骤

#### Step 1：判断任务类型，选对应模板

| 任务类型 | 选这个模板 |
|---|---|
| 实现一个 UI 页面（按原型还原） | `templates/页面开发-按原型.txt` |
| 实现一个完整功能（从 PRD 到测试） | `templates/功能开发-端到端.txt` |
| 修一个 Bug | `templates/修Bug.txt` |
| 写测试用例 | `templates/写测试.txt` |
| 评审一段代码 | `templates/代码评审.txt` |
| 新增 API（后端为主） | `templates/新增功能-后端.txt` |
| 新增页面（前端为主） | `templates/新增功能-前端.txt` |

#### Step 2：打开模板、复制内容、填任务卡

```
1. Cursor 中打开模板文件，如 templates/页面开发-按原型.txt
2. 全选复制（Cmd+A → Cmd+C）
3. 按 Cmd+I 打开 Composer
4. 粘贴模板
5. 在模板顶部的【任务卡】里填上你的具体信息
```

#### Step 3：让 Cursor 自动引用相关文件

Cursor 的强项是 `@` 引用。在 Composer 中用以下方式：

```
@docs/07-产品PRD-v2/02-采购会话核心模块.md     ← 引用 PRD
@docs/08-技术交付物/ui-prototype-pc/buyer/03-采购会话详情.html  ← 引用原型
@backend/huodaizi-session-service                ← 引用整个目录
@docs/08-技术交付物/api/openapi.yaml             ← 引用 API
@docs/08-技术交付物/db/01-schema.sql             ← 引用 DDL
```

**强烈建议**：每次任务都引用以下 5 个核心文件：

```
@docs/14-AI开发提示词/13-设计资产总目录.md
@docs/14-AI开发提示词/14-多规格红线.md
@docs/14-AI开发提示词/16-功能完整性checklist.md
@docs/07-产品PRD-v2/[对应模块].md
@docs/08-技术交付物/api/openapi.yaml
```

#### Step 4：等待 AI 输出"设计资产清单"

AI 应该**先输出资产清单，不直接写代码**。

✅ **正确的 AI 行为**：

```
我先定位本次任务的设计资产：

【本页设计资产清单】
- PRD：docs/07-产品PRD-v2/02-采购会话核心模块.md 第 4.1 节
- 原型（PC）：docs/08-技术交付物/ui-prototype-pc/buyer/03-采购会话详情.html
- 原型（移动端对照）：docs/08-技术交付物/ui-prototype/03-采购会话.html
- API：GET /api/v1/sessions/{id}（openapi.yaml#L156）
- 表：purchase_sessions, demand_cards, quotes
- 字段：sessionId, items[itemNo, productType, ...]
- 状态枚举：SessionStatus, DemandItem.status
- ...

请确认无误后我开始实现。
```

❌ **错误的 AI 行为**：

```
好的，我帮你实现这个页面...
（直接开始写代码）
```

**遇到错误行为**：立即打断，回复："**请先按 .cursorrules 要求输出设计资产清单，不要直接写代码**"

#### Step 5：审核资产清单

人工确认 AI 的清单是否：
- ✓ 引用的 PRD 章节正确
- ✓ 引用的原型对应你的需求
- ✓ 字段名都存在于 DDL
- ✓ 涉及的多规格场景已识别

发现遗漏：

```
回复 AI：你漏了 [xxx]，请补充
```

#### Step 6：让 AI 实现代码

```
回复 AI：清单 OK，请实现
```

Cursor Composer 会：
- 同时编辑多个文件
- 在右侧显示每个文件的 diff
- 你可以一个一个审核 Accept / Reject

#### Step 7：让 AI 自检

代码生成后，发送：

```
请按 6 维度自检并输出报告：
1. 设计资产引用
2. 多规格红线（@docs/14-AI开发提示词/14-多规格红线.md）
3. 端一致性（@docs/14-AI开发提示词/15-页面对应与不走样规范.md）
4. 167 功能完成度（@docs/14-AI开发提示词/16-功能完整性checklist.md 对应模块）
5. 50 条铁律（@docs/14-AI开发提示词/17-AI不能漏的50件事.md）
6. 16 维度验收（@docs/14-AI开发提示词/10-验收checklist.md）
```

AI 会逐项打勾或标记问题。

#### Step 8：人工抽查 + 测试

```
□ 用浏览器打开新页面，对照原型截图
□ 跑 mvn test（后端）/ npm test（前端）
□ 跑 Cursor 内置的 Lint
□ 关键场景手动测试一遍
```

#### Step 9：提交

```bash
git add .
git commit -m "feat(xxx): 实现 xxx 功能"
git push
```

---

## 三、常用场景实战

### 场景 A：实现一个 PC 端页面

**任务示例**：实现买家采购分析页（按 PC 端原型 buyer/08-采购分析.html）

**操作**：

```
1. Cmd+I 打开 Composer

2. 粘贴：
@docs/14-AI开发提示词/templates/页面开发-按原型.txt
@docs/08-技术交付物/ui-prototype-pc/buyer/08-采购分析.html
@docs/08-技术交付物/api/openapi.yaml
@docs/07-产品PRD-v2/08-买家工具包.md

【任务卡】
- 端：PC 端
- 原型：docs/08-技术交付物/ui-prototype-pc/buyer/08-采购分析.html
- 对应 PRD：docs/07-产品PRD-v2/08-买家工具包.md
- 路由：/buyer/analytics
- 技术栈：Vue 3 + Pinia + uni-app（PC 模式）

请按模板的 6 阶段开始。

3. 审核资产清单 → 让 AI 实现

4. Cursor 会创建：
   - frontend/src/pages/buyer/analytics/index.vue
   - frontend/src/api/analytics.js
   - frontend/src/stores/analytics.js
   - frontend/src/components/business/category-chart/index.vue

5. 让 AI 自检 + 写测试

6. 浏览器中打开 http://localhost:3000/buyer/analytics

7. 对照原型截图核对
```

### 场景 B：实现一个完整功能（端到端）

**任务示例**：实现"卖家批量报价"完整功能

**操作**：

```
1. Cmd+I 打开 Composer

2. 粘贴：
@docs/14-AI开发提示词/templates/功能开发-端到端.txt
@docs/07-产品PRD-v2/04-报价系统.md
@docs/08-技术交付物/api/openapi.yaml
@docs/08-技术交付物/db/01-schema.sql
@docs/08-技术交付物/ui-prototype-pc/seller/02-询价中心.html
@docs/08-技术交付物/ui-prototype/04-卖家接单.html
@backend/huodaizi-session-service

【任务卡】
- 功能：卖家批量报价（一次性对多行规格报价）
- PRD 章节：M4 报价系统
- 优先级：P0

请按模板的 7 阶段开始。

3. AI 会输出：
   Stage 1: PRD 理解 → 用户故事/业务规则/边界
   Stage 2: DDL 设计 → quotes 表字段
   Stage 3: OpenAPI 设计 → POST /api/v1/quotes（批量）
   ↑ 这里人工审核，确认无误
   Stage 4: 后端实现 → Entity/Service/Controller
   Stage 5: 双端前端 → PC 卖家中心 + 移动端接单
   Stage 6: 测试 → 单元 + 集成 + E2E
   Stage 7: 完整性核验

4. Cursor 会同时编辑：
   - backend/.../quote/entity/Quote.java
   - backend/.../quote/controller/QuoteController.java
   - backend/.../quote/service/impl/QuoteServiceImpl.java
   - frontend/src/pages/seller/quote-batch/index.vue
   - 测试文件

5. 跑 mvn test 验证
```

### 场景 C：修 Bug

**任务示例**：发现订单状态显示错误

**操作**：

```
1. Cmd+L 打开 Chat（不是 Composer，这是单文件操作）

2. 粘贴：
@docs/14-AI开发提示词/templates/修Bug.txt

【Bug 卡】
- Bug ID：BUG-2026-XXX
- 标题：买家订单列表中 "待发货" 显示为 "Pending"
- 严重级别：中
- 复现步骤：
  1. 登录买家端
  2. 进入"我的订单"
  3. 看到状态显示为英文"Pending"，应该是中文"待发货"

@frontend/src/pages/buyer/orders/index.vue

请按模板的 7 阶段处理。

3. AI 会先做根因分析，然后修

4. 关键：让 AI 写回归测试

5. 提交
```

### 场景 D：让 AI 评审你刚写的代码

**任务示例**：你写了一段代码想让 AI 帮你 review

**操作**：

```
1. Cmd+L 打开 Chat

2. 粘贴：
@docs/14-AI开发提示词/templates/代码评审.txt

@xxx.java（你刚写的文件）

请按 6 关卡评审。

3. AI 会按 6 个关卡输出报告，列出严重问题/建议项

4. 根据建议修改

5. 再请 AI 二次评审：
"请确认我已经修复了所有 Blockers"
```

### 场景 E：让 AI 检查整个模块的功能完整性

**任务示例**：M4 报价模块开发完后，确认是否漏功能

**操作**：

```
Cmd+L 打开 Chat：

@docs/14-AI开发提示词/16-功能完整性checklist.md
@backend/huodaizi-quote-service
@frontend/src/pages/seller/quote-management
@frontend/src/pages/buyer/quote-compare

请对照 16-功能完整性 checklist.md 的 M4 报价系统（18 项），
逐项检查我的代码是否实现，输出完成度报告。

未实现的项请列出理由 + 建议优先级。
```

---

## 四、Cursor 高级技巧

### 技巧 1：用 Symbols 引用（更精准）

```
@MyClass     ← 引用类
@myMethod    ← 引用方法
@MyFile.java ← 引用文件
```

### 技巧 2：用 Codebase 引用整个项目

```
@codebase 请告诉我整个项目目前对 DemandCard 字段的引用情况
```

### 技巧 3：用 Docs 引用文档

```
@docs/14-AI开发提示词/14-多规格红线.md 请按这份文档检查我的实现
```

### 技巧 4：分多轮对话保持上下文

不要把所有需求一次性砸给 AI，分阶段：

```
第 1 轮：需求理解 + 资产清单
第 2 轮：方案设计
第 3 轮：实现
第 4 轮：测试
第 5 轮：自检报告
```

### 技巧 5：当 AI 跑偏时立即纠正

```
AI 写出违反规则的代码 → 立即回复：

"你违反了 @docs/14-AI开发提示词/17-AI不能漏的50件事.md 的 [Axx] 条，
请按规则重新实现"
```

### 技巧 6：用 Cursor Rules 多文件叠加

除了 `.cursorrules`，可以在子目录加 `.cursorrules`：

```
backend/.cursorrules           只对后端生效
frontend/.cursorrules          只对前端生效
docs/.cursorrules              只对文档生效
```

### 技巧 7：把常用 Prompt 设为 Quick Prompt

```
Cursor → Settings → Quick Prompts

添加快捷 prompt：
- "按 50 条铁律评审本文件"
- "对照多规格红线检查"
- "输出 6 维自检报告"
- "对照 PC 端原型检查一致性"

用法：Cmd+K → 选择 Quick Prompt
```

---

## 五、不同场景的最佳实践

### 场景 P0：第一次开发某个模块

```
1. 让 AI 先读完整个 PRD 章节
   @docs/07-产品PRD-v2/02-采购会话核心模块.md
   请总结这个模块的核心业务流程和关键决策

2. 让 AI 列出本模块所有功能点
   @docs/14-AI开发提示词/16-功能完整性checklist.md
   请按 M2 列出 25 个功能点的优先级建议

3. 按优先级开发：先做 P0，再 P1，最后 P2

4. 每个功能开发用模板 templates/功能开发-端到端.txt
```

### 场景 P1：在已有代码基础上加功能

```
1. 先让 AI 读懂现有代码
   @backend/huodaizi-session-service
   请总结这个服务现有的功能和代码风格

2. 再用模板加功能
   @docs/14-AI开发提示词/templates/新增功能-后端.txt
   ...
```

### 场景 P2：紧急 Hotfix

```
1. 不走完整 7 阶段，但不能跳过：
   - 根因分析
   - 修复
   - 回归测试
   - 自检

2. 用简化模板：
   @docs/14-AI开发提示词/templates/修Bug.txt

3. 评审简化但必须有
```

---

## 六、常见问题 (FAQ)

### Q1：AI 还是不按规则来怎么办？

```
A：3 个升级动作：

1. 检查 .cursorrules 是否真的加载
   Cursor → Settings → Rules

2. 重启 Cursor

3. 在 Chat 中明确提醒：
   "请严格按 .cursorrules 中的规则工作。
    如果你不按规则，我会终止任务。"
```

### Q2：AI 输出的代码不能编译怎么办？

```
A：
1. 立即把错误信息粘给 AI：
   "编译错误：[粘贴错误]，请修复"

2. AI 修复后再次自检

3. 如果反复编译失败 → 换 AI 模型（Claude 3.5 → Claude 3.7）
```

### Q3：AI 输出太长怎么办？

```
A：用 Composer（多文件）而不是 Chat（单消息）

Composer 会自动把代码分到各个文件，不会被单消息长度限制
```

### Q4：AI 引用了错误的字段名怎么办？

```
A：
"你引用的字段 [xxx] 在 DDL 中不存在。
 请查 @docs/08-技术交付物/db/01-schema.sql 后重新实现"
```

### Q5：AI 把多规格写成单条怎么办？

```
A：这是最严重的违规。立即：

"你违反了 @docs/14-AI开发提示词/14-多规格红线.md。
 多规格不能退化为单条。
 请按 items 数组重新实现，并对照红线 4 层 17 条检查。"
```

### Q6：AI 写的页面与原型不一致怎么办？

```
A：
"请打开 @docs/08-技术交付物/ui-prototype-pc/buyer/08-采购分析.html，
 与你刚才写的代码逐项对照，
 列出差异并修复。"
```

### Q7：怎么让 AI 一次性实现多个相关页面？

```
A：用 Composer + 一次任务说清楚：

@docs/14-AI开发提示词/templates/页面开发-按原型.txt

请同时实现以下 3 个页面（都对应同一 API 模块）：
1. PC 端 buyer/06-清单管理.html
2. 移动端 12-买家我的清单.html
3. 公共组件 ListCard.vue（两端复用）

请按模板对每个页面分别走完 6 阶段。
```

### Q8：怎么验证 AI 已经看了我引用的文档？

```
A：在任务开始时问：

"在开始编码前，请告诉我：
 @docs/07-产品PRD-v2/02-采购会话核心模块.md 第 4.1 节
 描述了什么内容（用 50 字）？"

如果回答不准确 → 强制重新读文档
```

---

## 七、效率提升 Tips

### Tip 1：建立你的 Quick Prompt 库

```
设置位置：Cursor → Settings → Quick Prompts

推荐添加：

[QP1] "请先输出设计资产清单，不要直接写代码"
[QP2] "请按 50 条铁律自检本次代码"
[QP3] "请对照对应另一端原型检查一致性"
[QP4] "请用 MapStruct 而非 BeanUtils.copyProperties"
[QP5] "请把这个查询改成分页"
[QP6] "请把这个同步调用改成 MQ 异步"
```

### Tip 2：建立你的开发日志

每次任务前在 `开发日志.md` 记录：

```markdown
## 2026-05-27 任务：实现买家采购分析

【模板】templates/页面开发-按原型.txt
【对应原型】buyer/08-采购分析.html
【AI 资产清单输出】正确 ✓
【AI 实现】生成 5 个文件
【AI 自检】通过 6 维度
【人工抽查】发现 2 处需调整
【提交】commit xxx
【耗时】3 小时（vs 传统 8 小时）
```

### Tip 3：每周整理 AI 翻车 case

```
建立 ai-错题本.md：

记录每次 AI 翻车的具体场景：
- 任务：xxx
- AI 输出：xxx
- 问题：违反了 [Axx] 条
- 修复：xxx
- 教训：xxx

→ 每月更新一次提示词，把翻车 case 加到反模式
```

### Tip 4：用 Cursor 的 Apply 智能审核

```
AI 写完代码后，不要直接 Accept All

逐文件查看：
- 重要文件：仔细 review
- 简单文件：快速过

特别关注：
- 是否引用了正确字段名
- 是否覆盖了多规格
- 是否漏功能
```

---

## 八、推荐每日工作流

```
9:00  打开 Cursor，挑选今日任务
9:15  对照 16-功能完整性 checklist 确定优先级
9:30  开发任务 1（用模板）
12:00 午休
13:30 开发任务 2
16:00 让 AI 自检本日所有代码
17:00 写测试 + 提 PR
17:30 整理 AI 错题本

→ 用提示词工程后，AI 辅助效率 3-5 倍
```

---

## 九、紧急情况下的"逃生包"

如果遇到 AI 完全不按规则、或仓库环境出问题：

### 9.1 重置 Cursor 状态

```
1. Cursor → Settings → 重置所有规则
2. 关闭 Cursor
3. rm -rf ~/.cursor/extensions（如果是 mac）
4. 重新打开 Cursor
5. 重新加载 .cursorrules
```

### 9.2 换 AI 模型

```
Claude 3.5 Sonnet 翻车 → 试 Claude 3.7
Claude 系列翻车 → 试 GPT-4o
GPT-4o 翻车 → 试 通义千问 / Cursor Composer
```

### 9.3 简化任务

```
AI 反复出错 → 任务太复杂 → 拆分：

把"实现卖家完整工作流" 拆成：
1. 实现卖家询价列表（一个页面）
2. 实现卖家询价处理（一个页面）
3. 实现卖家报价管理（一个页面）
...
```

### 9.4 找人工接管

```
反复 3 次 AI 翻车 → 暂停 AI → 手动实现关键骨架 → 再让 AI 补充细节
```

---

## 十、总结：一句话使用法

```
1. 永远先 @ 引用相关文档（PRD/DDL/API/原型/提示词）
2. 永远先要求 AI 输出"设计资产清单"
3. 永远在结束前要求 AI 输出"6 维自检报告"
4. 永远人工抽查关键代码
5. 永远写测试验证
```

按这 5 条，AI 开发的代码质量能稳定在 90% 以上。

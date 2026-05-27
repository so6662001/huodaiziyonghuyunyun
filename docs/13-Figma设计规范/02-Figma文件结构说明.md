# Figma 文件结构说明

> 给设计师的 Figma 工程组织规范。

## 一、Figma 工程总结构

建议建一个 Team 下的 Project：「货袋子产品设计」

```
货袋子产品设计/
├── 📚 00 - 设计系统（Library）
│   ├── Tokens（颜色/字体/间距）
│   ├── 基础组件（Button/Input/Card）
│   ├── 业务组件（询价卡/报价卡）
│   └── 图标库
│
├── 📱 01 - 买家端（小程序）
│   ├── 首页（双入口）
│   ├── 发需求流程
│   ├── 清单上传流程
│   ├── 采购会话
│   ├── 报价对比
│   ├── 我的（买家版）
│   └── 设置/资料
│
├── 🏭 02 - 卖家端（小程序）
│   ├── 卖家中心
│   ├── 我的库存
│   ├── 我的询价
│   ├── 报价/议价
│   ├── CRM（我的客户）
│   └── 收益看板
│
├── 💼 03 - 大客户 SaaS（Web）
│   ├── Dashboard
│   ├── 供应商管理
│   ├── 项目档案
│   └── 比价单管理
│
└── 🔧 04 - 后台管理（Web）
    ├── 用户管理
    ├── 风控管理
    ├── 数据看板
    └── 内容管理
```

## 二、命名规范

### 2.1 页面命名

```
页面命名：[端]-[模块]-[页面名]

示例：
  买家-发需求-极简版
  买家-清单上传-AI识别
  卖家-我的询价-列表
```

### 2.2 Frame 命名

```
Frame 命名：[页面名]-[状态/版本]

示例：
  发需求-默认状态
  发需求-填写中
  发需求-提交后
  发需求-加急悬赏版
```

### 2.3 组件命名

```
组件命名：[级别]/[组件类型]/[变体]

示例：
  基础/Button/Primary
  基础/Input/Default
  业务/Card/询价卡
  业务/Card/库存匹配
```

## 三、组件库设置

### 3.1 必备组件清单

#### 基础组件（约 30 个）

```
按钮：
  - Button/Primary/Large
  - Button/Primary/Medium
  - Button/Primary/Small
  - Button/Secondary/Large
  - Button/Secondary/Medium
  - Button/Secondary/Small
  - Button/Warning
  - Button/Danger
  - Button/Ghost

输入：
  - Input/Default
  - Input/Focus
  - Input/Error
  - Select/Default
  - Checkbox/Default
  - Radio/Default
  - Switch/On
  - Switch/Off

卡片：
  - Card/Default
  - Card/Hover

标签：
  - Tag/Primary
  - Tag/Success
  - Tag/Warning
  - Tag/Danger
  - Tag/Gold（S 级专用）
  - Chip/Default
  - Chip/Active

通知：
  - Toast/Success
  - Toast/Error
  - Toast/Info
  - Banner/Info

加载：
  - Spinner/Default
  - Skeleton/Card
  - Skeleton/Line
```

#### 业务组件（约 20 个）

```
需求/报价：
  - 需求卡片/默认
  - 需求卡片/已变更
  - 报价卡片/默认
  - 报价卡片/Top1（金色）
  - 报价卡片/优质（蓝色）
  - 配置器/数量选择
  - 配置器/规格选择
  - 配置器/加项选择

库存：
  - 库存卡片/默认
  - 库存匹配标签

卖家：
  - 卖家信用分（5 星 + 数字）
  - 卖家分层标签（S/A/B/C）
  - 买家分层标签（主力/活跃/新/询价党）

时间线：
  - 时间线节点
  - 时间线连接线
  - AI 识变确认条
```

### 3.2 Variants 配置

每个组件用 Figma Variants 配置变体：

```
Button：
  - Type: Primary / Secondary / Warning / Danger / Ghost
  - Size: Large / Medium / Small
  - State: Default / Hover / Active / Disabled

Card：
  - Type: Default / Premium / Highlight
  - State: Default / Hover

Tag：
  - Color: Primary / Success / Warning / Danger / Neutral / Gold
```

## 四、Auto Layout 规范

### 4.1 必须用 Auto Layout 的场景

```
✓ 列表（所有 list）
✓ 表单（form）
✓ 卡片内部结构
✓ 按钮组
✓ 标签组
✓ 导航栏
```

### 4.2 Auto Layout 间距

```
内部间距：
  紧凑：8px
  默认：12px
  宽松：16px

子元素间距：
  小：4px
  默认：8px
  大：12px
```

## 五、Components 标注规范

每个组件必须有：

```
1. 描述（Description）
   告诉使用者什么时候用

2. Props 说明
   - text: 按钮文字
   - icon: 是否带图标
   - state: 默认/hover/disabled

3. 使用示例（链接到使用页面）
```

## 六、设计稿交付规范

### 6.1 给开发的标注

```
使用 Figma 自带的 Inspect 模式：
  - 自动生成 CSS
  - 颜色 hex 值
  - 字号 + 行高
  - 间距数值
  - 圆角数值
  - 阴影值

开发可以直接复制 CSS 使用。
```

### 6.2 切图导出

```
图标：SVG 格式（推荐）
图片：WebP（首选）或 PNG 2x

命名：
  icon_xxx.svg
  img_xxx.webp

导出位置：
  Figma → Export → 设置 2x / 3x
```

### 6.3 关键页面交付清单

每个页面必须交付：

```
□ Figma 链接（含 Inspect 模式）
□ 各端切图（移动 / iPad / 桌面如需）
□ 字体清单
□ 图标清单
□ 交互说明（点击 / 滑动 / 加载等）
□ 边界状态（空状态 / 错误状态 / 加载状态）
```

## 七、版本管理

```
Figma 自带版本历史，但建议：

主要版本节点（必须命名）：
  v1.0 - MVP 设计完成
  v1.5 - 双引擎过渡设计
  v2.0 - 全功能版本
  v2.1 - 优化迭代

每次发版前：
  1. 创建版本快照
  2. 命名 vX.X
  3. 添加 changelog 注释
  4. 通知开发团队
```

## 八、协作流程

```
1. 设计师在 Figma 中设计
2. 与产品在 Figma 评审（直接评论）
3. 设计 Lock 之前先与开发对齐技术可行性
4. 开发用 Inspect 模式获取标注
5. 开发自测时使用 Figma 切图
6. 验收时设计师在 Figma 中标注差异

注意：
  - Figma 链接所有人可读
  - 修改权限仅设计师 + PM
  - 历史版本永不删除
```

## 九、字体加载

钢贸老板手机不一定能渲染 PingFang，需要 fallback：

```
font-family:
  -apple-system,           # iOS
  BlinkMacSystemFont,      # Mac
  "PingFang SC",           # iOS / Mac 中文
  "Microsoft YaHei",       # Windows / Android
  sans-serif;              # 兜底
```

Figma 设计时使用 PingFang SC，开发时按上述 stack 实现。

## 十、深色模式

```
v1 不做深色模式。
v2 视情况补充（钢贸老板很少用深色模式）。

如果做，请在 Figma 中：
  - 创建 Dark Variant
  - 共享同一份 Tokens
  - 自动切换颜色
```

## 十一、Figma 插件推荐

```
必装：
  - Figma Tokens（导入 design-tokens）
  - Iconify（海量图标）
  - Stark（无障碍检查）
  - Content Reel（中文假数据）

可选：
  - Pitchdeck Slides（PPT 导出）
  - HTML to Figma（HTML 转 Figma，可用于参考已有原型）
  - Material Theme Builder（颜色辅助）
```

## 十二、设计师必读清单

```
新设计师入职前 3 天必读：

Day 1:
  □ docs/07-产品PRD-v2/00-PRD总览.md
  □ docs/13-Figma设计规范/01-设计系统总览.md
  □ 浏览所有 9 个 HTML 原型（理解功能）

Day 2:
  □ docs/13-Figma设计规范/02-Figma文件结构说明.md（本文档）
  □ 学习 Figma Tokens 插件
  □ 复现 1 个简单页面（练手）

Day 3:
  □ 与 PM 1 对 1
  □ 与开发对齐技术约束
  □ 接手第一个设计任务
```

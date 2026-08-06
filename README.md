# Pixel UI Maker

> 像素风 UI / CSS 主题制作器 —— 一个 [Claude Code](https://claude.com/claude-code) 技能，把界面描述、线框图或参考设计转换为完整的像素艺术 UI 实现（CSS + 组件标记），并保持严格统一的视觉风格。

覆盖**像素按钮与交互**、**像素背景**、**容器窗口**和**样式交互动画**四大组件家族，全部锁定在同一套视觉契约之下。

> 🌐 English version: [README.md](README.md)

---

## 它能做什么

输入一段界面描述、线框图或现有的 CSS / 参考截图，该技能会产出：

1. **UI 设计规范**（`ui_spec.md`）—— 主题名称、像素风格、调色板、样式锁参数、组件清单和动画方案。
2. **CSS 实现**（`theme.css` 或按家族拆分）—— 使用 `--pix-*` 自定义属性与 `pix-` 前缀组件类。
3. **验证** —— 自动检查每个组件是否遵守样式锁规则。

核心产出形态示例：

```css
:root {
  --pix-color-bg:        #111111;
  --pix-color-surface:   #1E1E1E;
  --pix-color-accent:    #5D8BFF;
  --pix-space-1: 4px;  --pix-space-2: 8px;
}

.pix-btn {           /* 按钮交互 */
  border: 2px solid var(--pix-color-accent-edge);
  border-radius: 2px;
  box-shadow: 0 4px 0 var(--pix-color-accent-shadow);  /* 硬边 3D 立体感 */
  transition: transform 60ms linear, box-shadow 60ms linear;
}
.pix-btn:active {
  transform: translateY(3px);
  box-shadow: 0 1px 0 var(--pix-color-accent-shadow);  /* 按下时沿硬边下沉 */
}
```

---

## 何时使用

当请求中提到以下任一关键词时，调用本技能：

- "pixel-style the UI"、"make a pixel theme"、"generate pixel CSS"
- **像素风界面**、**像素样式开发**、**像素按钮**、**像素背景**、**像素窗口**
- `pixel-ui-maker`

典型场景：登录页、仪表盘、设置面板、游戏 UI、复古风格作品集 —— 支持 Vue、React、纯 HTML+CSS 或小程序。

---

## 工作原理

技能按照 **5 步串行管线**执行。每一步的输出是下一步的输入；两处 "gate" 会在等待用户确认时强制停下。

```
输入（界面描述 + 需求）
   │  第 1 步 · 输入收集
   ▼
设计规范  ──────────── 第 2 步 · 设计规范制定
   │  ⛔ BLOCKING 门
   ▼
风格确认  ──────────── 第 3 步 · 用户审阅并批准 UI 规范
   │  🚧 门
   ▼
实现生成  ──────────── 第 4 步 · 生成 CSS + 组件标记
   │
   ▼
验证与交付 ──────────── 第 5 步 · style_validator.py + 导出
```

| 步骤 | 产出 | 门 |
|------|------|-----|
| 1. 输入收集 | 结构化需求（界面、组件、风格方向、框架） | 🚧 |
| 2. 设计规范制定 | `ui_spec.md` —— 调色板、样式锁参数、组件清单、动画方案 | 🚧 |
| 3. 风格确认 | 已批准的规范 | ⛔ **BLOCKING** —— 等待用户批准 |
| 4. 实现生成 | CSS + 可选组件标记 | 🚧 |
| 5. 验证与交付 | 验证通过的主题、`validation.json` | 🚧 |

> ⚠️ **执行纪律**：步骤必须严格按顺序执行；禁止跨阶段提前准备；所有组件保持风格一致是最高优先级。

---

## 核心概念

### 样式锁（Style Lock，严格规则）

生成的每个组件**必须**满足以下全部规则 —— 这是本技能的核心：

| 规则 | 约束 |
|------|------|
| **调色板** | 只用声明过的 HEX 颜色 |
| **圆角** | `border-radius` 只能是 0–2px，禁止柔和圆角 |
| **边框** | 整数 px 粗细，按组件类型保持一致 |
| **阴影** | 只能 HARD：`box-shadow: <offsetX> <offsetY> <color>` —— 无模糊/扩散半径 |
| **渐变** | 填充禁止渐变；允许硬边的 `repeating-*` 纹理图案 |
| **透明度** | 只能是 0 或 1（阶梯式遮罩除外） |
| **模糊** | 禁止 `filter: blur(...)` |
| **栅格** | 所有间距必须是基准单位（如 4px）的整数倍 |
| **字体** | 等宽或像素字体；像素字体关闭 `font-smoothing` |
| **图片** | 栅格资源使用 `image-rendering: pixelated` |
| **动效** | 用 `steps()` 离散步进或短 linear；禁止弹性/ease-in-out 过冲；必须带 `prefers-reduced-motion` 降级 |
| **命名** | `pix-` 类前缀、`--pix-*` 自定义属性 |

### 四大组件家族

| 家族 | 覆盖组件 |
|------|----------|
| **按钮交互** | `pix-btn` 默认/hover/active/focus-visible/disabled 状态、`[aria-pressed]` 开关、变体（solid / outlined / ghost / danger / success）、尺寸（`--sm` 32px / `--md` 40px / `--lg` 48px）、`pix-btn-group` |
| **背景** | 纯色、棋盘格、网格线、抖动填充、噪点/扫描线、暗角、瓷砖边框 |
| **容器窗口** | `pix-window`（标题栏 + 内容区 + 窗口按钮）、`pix-panel`（+ raised/sunken）、`pix-card`、`pix-modal` |
| **交互动画** | 弹出/收起、按压机制、待机上下浮动、抖动、焦点环、加载动画、环境循环 —— 全部步进式 |

> 完整的生成契约（按钮按压机制、背景配方、窗口结构、关键帧配方）见 [`references/generator-pixel-ui.md`](references/generator-pixel-ui.md)。

---

## 脚本

[`scripts/`](scripts/) 下有三个独立的 Python 脚本，**仅使用 Python 标准库 —— 无需安装任何依赖**（`requirements.txt` 刻意为空）。

### palette_extractor.py —— 从 CSS 文件提取 HEX 颜色

```bash
python scripts/palette_extractor.py theme.css                          # 按使用频率列出颜色
python scripts/palette_extractor.py theme.css --format json            # 输出带占比的 JSON
python scripts/palette_extractor.py theme.css --analyze-only           # 只分析，不列调色板
python scripts/palette_extractor.py theme.css --format json --output palette.json
```

### style_validator.py —— 按样式锁规则校验 CSS 文件

```bash
python scripts/style_validator.py theme.css --palette "#111111" "#1E1E1E" "#5D8BFF"
python scripts/style_validator.py theme.css --spec ui_spec.md --grid 4 --prefix pix-
python scripts/style_validator.py theme.css --spec ui_spec.md --strict          # 警告也视为失败
python scripts/style_validator.py theme.css --spec ui_spec.md --output validation.json
```

检查项：调色板归属、`border-radius` ≤ 2px、无渐变填充、仅硬阴影、无 `filter: blur`、透明度二值化、间距为栅格整数倍、`pix-` 前缀契约。**退出码 0 = 通过，1 = 未通过。**

### theme_scaffolder.py —— 从 `ui_spec.md` 生成 `theme.css` 骨架

```bash
python scripts/theme_scaffolder.py ui_spec.md --output theme.css
python scripts/theme_scaffolder.py ui_spec.md --print                   # 输出到标准输出
```

解析规范中的调色板和样式表生成 `:root` 变量，再输出组件脚手架，作为第 4 步的起点。

---

## 模板

| 模板 | 用途 |
|------|------|
| [`templates/ui_spec.md`](templates/ui_spec.md) | 人类可读的设计文档：主题信息、视觉描述、调色板表、样式定义、组件清单、动画方案、输出配置 |
| [`templates/ui_implementation_prompt.md`](templates/ui_implementation_prompt.md) | 用于生成 CSS 实现的结构化提示词模板，含逐家族组件规格 |

---

## 工作流（独立使用）

不属于主管线 —— 常见后续任务的复用清单：

| 工作流 | 适用场景 |
|--------|----------|
| [`workflows/extend-theme.md`](workflows/extend-theme.md) | 为**现有**像素主题添加新组件，同时保持样式锁一致 |
| [`workflows/from-reference.md`](workflows/from-reference.md) | 基于**参考**截图、线框图或现有 CSS 派生主题 |

---

## 命名契约

所有生成的主题必须遵循（验证器和脚手架依赖此契约）：

- **类前缀**：`pix-` → `.pix-btn`、`.pix-window`、`.pix-bg--checker`
- **自定义属性**：`--pix-*` → `--pix-color-accent`、`--pix-space-2`、`--pix-motion-enter`

---

## 输出结构

单文件模式（`theme.css`）或多文件模式（每个家族一个 CSS）：

```
output/<theme_name>_<timestamp>/
├── theme.css              # :root 变量 + 全部组件
├── components/            # 可选，按家族拆分
│   ├── buttons.css
│   ├── backgrounds.css
│   ├── windows.css
│   └── animations.css
├── ui_spec.md             # 最终规范
├── theme_manifest.json    # 主题名、调色板、栅格、文件映射（多文件模式）
└── validation.json        # style_validator.py 输出
```

---

## 环境要求

- **Claude Code**，技能安装在 `~/.claude/skills/pixel-ui-maker/` 下。
- **Python 3** 用于验证/脚手架脚本 —— 无需第三方包。

---

## 相关技能

- **pixel-entity-maker** —— 配套技能，负责像素*角色 / 动画精灵*（精灵图）。当需求涉及角色和序列帧而非 UI 组件时使用。

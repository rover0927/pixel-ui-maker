# CYBER-GEEK — 黑客赛博朋克个人主页 Design Spec

> 暗黑终端极客 geek lock 的赛博朋克变体：近黑深空底 + 霓虹青主强调 + 霓虹洋红辅强调，0 圆角锐利几何、红色角标→青色角标、CRT scanline / glitch / typewriter 终端 motif、霓虹光晕与平滑动效。内置 JIEJOE 蒸馏动态效果：`geek-btn-wipe` / `geek-float-rise` / `geek-marquee` / `geek-crt-ripple`。

---

## I. Theme Information

| Field | Value |
|-------|-------|
| **Name** | cyber-geek |
| **Target Interface** | 个人主页（单页，长滚动） |
| **Platform / Framework** | Vue 3 + Vite（Composition API） |
| **Geek Style** | 暗黑终端极客 × 黑客赛博朋克（自定义） |
| **Spacing base** | 4px（整数 px，松散非严格网格） |
| **Target Use** | 个人作品集主页 |

---

## II. Visual Description

```
- Overall mood: 黑客终端 · 赛博夜城。近黑深空画布 + 霓虹青(#00f0ff)主强调 + 洋红(#ff2bd6)辅强调
- Layout: 固定顶栏 nav / hero / about / skills / projects / photos / contact / footer
- Component list: nav(logo+menuicon+contact), hero(glitch title+typewriter+CRT屏+粒子网络+浮动像素画),
  window终端卡, tag技能墙, timeline项目时间线, 照片拍立得板, 联系表单, marquee分割带
- Distinctive features: 青色 corner 角标、// eyebrow 标签、CRT scanlines、glitch 标题、
  typewriter 光标、霓虹光点、双层擦除按钮、像素粒子网络背景、像素画错峰上浮、四向滚动光带、CRT 水波纹
- Background treatment: 56px 青色网格 + 径向霓虹光晕 + 像素粒子网络 canvas + scanlines 叠加
```

---

## III. Color Palette

| Index | HEX | Role | Used On |
|-------|-----|------|---------|
| 0 | `#05070c` | Background | 页面根 (`--geek-color-bg`) |
| 1 | `#0a0f18` | Surface | 卡片/窗口 (`--geek-color-bg-soft`) |
| 2 | `#1b2634` | Line | 1px 发丝边框 (`--geek-color-line`) |
| 3 | `#00f0ff` | 主强调(青) | 角标/按钮/glitch/active nav (`--geek-color-red`) |
| 4 | `#e6f1ff` | Text primary | 标题/正文 (`--geek-color-text`) |
| 5 | `#9fb2c8` | Text secondary | 副标题/meta (`--geek-color-text-dim`) |
| 6 | `#5b6b80` | Text muted | 注释/行号 (`--geek-color-text-mute`) |
| 7 | `#00ffd5` | Teal | 成功/在线 (`--geek-color-teal`) |
| 8 | `#2e7dff` | Blue | 链接/信息 (`--geek-color-blue`) |
| 9 | `#ffd500` | Amber | 警告 (`--geek-color-amber`) |
| 10 | `#ff2bd6` | Crimson→洋红 | 危险/霓虹辅强调 (`--geek-color-crimson`) |
| 11 | `#04070c` | CRT screen | CRT 屏幕底色（比页面根更深的近黑）(`--geek-color-crt`) |

**Total colors**: 11

> 光晕：青 `0 0 24px rgba(0,240,255,.35)` · 洋红 `0 0 24px rgba(255,43,214,.35)` ·
> 卡片 `0 8px 32px rgba(0,0,0,.55)`

---

## IV. Style Definition

| Property | Value |
|----------|-------|
| **Corner radius** | 0px 全部盒（点 50%、滚动条 8px、代码 2px） |
| **Border weight** | 1px 发丝线（青/洋红/文字色） |
| **Shadow style** | 柔和 + 霓虹光晕（青/洋红双色可选） |
| **Hover lift** | 按钮 `translateY(-2px)` / 卡片 `translateY(-4px)` |
| **Gradients** | 56px 青色网格、CRT scanlines、径向霓虹光晕 |
| **Focus ring** | `outline: 3px solid 青`, `outline-offset: 2px` |
| **Spacing** | 整数 px，松散步进 4px |
| **Transition** | `.2s ease` 颜色 / `.3s ease` 位移 / `.6s ease` 缩放 / `.8s ease` 滚入 |
| **Fonts** | mono（JetBrains Mono / Fira Code）用于标签/按钮/数字；sans 用于正文/标题 |

---

## V. Component Inventory

### A. 顶栏 nav（fixed）
| Component | 说明 |
|-----------|------|
| `geek-nav` | fixed 顶栏，`backdrop-filter: blur(14px) saturate(140%)`，下缘 1px 青色发丝线 |
| `geek-nav__logo` | 左上 logo，mix-blend-mode:difference，hover 青 glow |
| `geek-nav__menuicon` | 汉堡↔X 变形（stroke-dasharray + rotate），`.4s ease` |
| `geek-nav__contact` | **`geek-btn-wipe`** 双层擦除按钮（导航栏 CONTACT） |

### B. Hero
| Component | 说明 |
|-----------|------|
| `geek-hero` | 100vh，56px 青色网格 + 径向霓虹光晕背景 |
| `geek-particle-bg` | 最底层 canvas 像素方块粒子网络：慢速漂浮 + 近邻连线 + 鼠标排斥/青色光标连线（`useParticleBg.js`，DPR≤2，reduced-motion 静态帧） |
| `geek-float-rise` | 背景像素画 SVG 图块，载入时 `stagger 120ms` 错峰上浮（`geek-float-rise--active`） |
| `geek-hero__title` | glitch 标题（红青 clip-path 切片，`steps(1)` 3s） |
| `geek-hero__sub` | typewriter 打字副标题 + 光标 `1s steps(1)` |
| `geek-screen` | CRT 屏：`filter: url(#geek-crt-ripple)` + scanlines 叠加 + 状态日志 |
| `geek-hero__scrolltip` | 底部滚动提示（青 ↑） |

### C. About — `geek-window` 终端卡
`__title` 4px 青色顶栏 + mono 标题 + `[×]`；正文 typewriter 输出 `whoami / sysinfo / skills` 行。

### D. Skills — `geek-tag` 墙 + 青色进度条
| 类 | 说明 |
|----|------|
| `geek-tag` | mono 12px，0 圆角，霓虹状态色 + 13% alpha 底 |
| `geek-bar` | 技能条：青色渐变填充 + 霓虹光晕 + mono 百分比 |

### E. Projects — `geek-timeline` + `geek-card`
| 类 | 说明 |
|----|------|
| `geek-timeline` | 竖直青色渐变线 + 11px 霓虹光点，hover 洋红光晕 |
| `geek-card` | `.corner` 青色角标、hover `translateY(-4px)` + 青色描边 + 深影 |

### F. Photos — 拍立得板 + marquee 分割带
| 类 | 说明 |
|----|------|
| `geek-photos` | 5 张扇形排布拍立得板（`transform-origin: bottom left`），hover 图 `scale(1.1)` `.6s` |
| `geek-marquee` | 四向滚动光带分割带（`// SYSTEM ONLINE · ACCESS GRANTED ·`） |

### G. Contact — 表单 + 擦除提交
| 类 | 说明 |
|----|------|
| `contact_form` | 青色表单窗，输入框 hover 洋红边框 |
| `geek-btn-wipe` | 提交按钮（SUBMIT + 箭头）双层擦除 |

### H. Footer
`geek-footer`：marquee + `// © 2026 CYBER-GEEK` 版权行。

### I. Interaction Animations
| 交互 | 动效 | 曲线 | 时长 |
|------|------|------|------|
| 按钮 hover | 反色 + 上浮 + 光晕 | ease | .2s/.3s |
| `geek-btn-wipe` | 双层擦除 + 标签/箭头滑动 | ease | .4s（chase .1s） |
| `geek-float-rise` | 图块 `translateY(100%)→0` stagger 120ms | ease | .8s |
| `geek-particle-bg` | 像素方块漂浮 + 近邻连线 + 鼠标排斥/连线 | rAF | — |
| `geek-marquee` | 四向滚动光带 | linear | 8s infinite |
| `geek-crt-ripple` | SVG turbulence + rAF seed/scale | — | — |
| 卡片 hover | 上浮 + 描边 + 深影 | ease | .3s |
| 滚入 reveal | fadeUp opacity+translateY24 | ease | .8s |
| typewriter 光标 | blink | steps(1) | 1s infinite |
| glitch | clip-path 切片 | steps(1) | 3s infinite |

---

## VI. Output Configuration

| Option | Value |
|--------|-------|
| **Output mode** | 单 `theme.css`（`src/assets/geek-homepage.css`）+ 组件拆分注释段 |
| **Custom properties** | `--geek-*` 前缀于 `:root` |
| **Class prefix** | `geek-` |
| **Framework markup** | Vue 3 组件（App.vue + 分节组件） |
| **Reduced motion** | 含 `prefers-reduced-motion` 回退 |

---

## VII. Build & Run

```
npm install
npm run dev    # Vite dev server
npm run build  # 产物到 dist/
```

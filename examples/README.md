# Examples — 示例

pixel-ui-maker 的可运行示例。所有示例遵循 geek 样式锁,并带 `prefers-reduced-motion` 降级。

## 统一约定

- 子目录示例(Vue 3 + Vite)统一结构:`src/{components,composables,assets}` + `index.html` + `vite.config.js` + `README.md` + `package.json`,可独立 `npm install && npm run dev`。
- 组件统一 `Geek*` PascalCase(映射 `geek-*` CSS 类),composables 统一 `use*` camelCase,主题资产统一 `geek-<name>.css`。
- 每个 Vue 示例对应一份 `references/` 配方文档与一份项目内 `ui_spec.md`;源码与 `references/` 文档保持一致。
- 扁平 HTML + CSS 示例(无构建)直接打开 HTML 预览。

## 索引

| 示例 | 类型 | 路径 | 内容 | 运行 |
|------|------|------|------|------|
| geek 蒸馏动效 | 静态 HTML + CSS | `geek-effects-demo.html` (+ `.css`) | 双层擦除按钮 `geek-btn-wipe`、背景像素画错峰上浮 `geek-float-rise`、四向滚动光带 `geek-marquee`、CRT 水波纹 `geek-crt-ripple` | 直接打开 HTML 预览 |
| 流体网格像素背景 | Vue 3 + Vite | `fluid-grid-bg/` | 双引擎 canvas 像素网格背景:`useFluidGrid`(噪声/波浪/涡流流场 + 鼠标漩涡·排斥)+ `useDisturbanceWave`(统一像素 + 双噪声场 + 呼吸潮汐);实时控制面板 + `geek-copy-params` 复制参数按钮 | `cd fluid-grid-bg && npm install && npm run dev` |
| 黑客赛博朋克个人主页 | Vue 3 + Vite | `geek-homepage/` | CYBER GEEK 个人主页:`GeekHero` glitch + 打字机 + CRT 屏、粒子网络背景、四向滚动光带、霓虹像素拍立得、双层擦除按钮等 11 组件 + 3 composables;内含 JIEJOE 蒸馏动态效果 | `cd geek-homepage && npm install && npm run dev` |
| 背景工具包画廊 | 静态 HTML | `index.html` | 全部 8 个动态背景效果目录:类名 · 说明 · 触发 · 来源 · 预览链接(静态 demo 直接看,Vue demo 给 `npm install && npm run dev` 指引) | `python ../scripts/preview_backgrounds.py` 打开 `http://localhost:8000/` |
| 核心组件展示 | 静态 HTML + CSS | `components.html` | 调色板色卡 + 按钮(primary/ghost/danger/尺寸/禁用) + 卡片/窗口/标签 + 签名 motif(`//` 眉题/角标/glitch/光标/时间线),展示 `geek-` 核心组件家族 | 直接打开 HTML 预览 |

> 效果配方见 `references/dynamic-effects.md` 与 `references/background-fluid-grid.md`;个人主页内置的 JIEJOE 动效是 `dynamic-effects.md` 的完整 Vue 实现。
>
> 画廊页 `index.html` 与核心组件展示 `components.html`、动态效果 demo `geek-effects-demo.html` 都由 `preview_backgrounds.py` 托管,也可直接双击用浏览器打开(`file://` 可用)。两个 Vue demo(`geek-homepage` / `fluid-grid-bg`)不会被预览服务器启动,仅给出 `npm install && npm run dev` 指引。

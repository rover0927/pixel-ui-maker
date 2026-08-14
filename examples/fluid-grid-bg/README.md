# 流体网格像素背景 — Fluid Grid BG Vue Demo

按《流体网格粒子动画效果实现指南》实现的 Vue 3 + Vite demo:
固定网格 + 流场驱动 + 颜色映射 + 呼吸闪烁,附带鼠标扰动与实时参数面板。

## 运行

```bash
npm install
npm run dev     # 开发预览
npm run build   # 构建产物
```

## 结构

```
src/
  composables/useFluidGrid.js       # 引擎 A：固定网格流体动画引擎（noise/wave/vortex + 鼠标扰动）
  composables/useDisturbanceWave.js # 引擎 B：固定像素点阵 + 双噪声场 + 呼吸潮汐（无鼠标）
  components/GeekFluidGrid.vue      # 背景画布组件，按 flowMode 切换引擎
  App.vue                           # 演示页面 + 控制面板（含复制参数按钮）
  assets/geek-fluid-grid.css        # 暗色终端像素风样式
```

## 干扰波模式（flowMode: 'disturb'）

统一大小的像素点阵（位置/尺寸跟随「网格大小 / 间隙」），方块只表现「亮不亮 + 颜色变化」。
**双噪声场分层** —— 亮度场驱动细腻光斑游走，颜色场驱动米白 #f8f6e8 ↔ 主题主色
平滑渐变，两场各自独立漂移；叠加**呼吸潮汐**（整屏明暗起伏，速度跟随「呼吸频率」）。
可调参数：颜色主题、呼吸频率、流动速度、亮度、网格大小 / 间隙；无流向色偏、无鼠标交互。
色调低亮、柔和不突兀，无干扰线扫过。纯黑背景。

## 关键参数（引擎 options）

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `cellSize` | 10 | 小方块尺寸(px) |
| `gap` | 2 | 方块间隙(px) |
| `maxPixels` | 4500 | 像素点上限,超限自动加粗网格 |
| `flowSpeed` | 0.06 | 流场漂移速度 |
| `flowMode` | `noise` | `noise` 噪声场 / `wave` 波浪场 / `vortex` 涡流场 / `disturb` 干扰波 |
| `flicker` | 1.4 | 呼吸闪烁频率 |
| `brightness` | 1.0 | 整体亮度倍率 |
| `hue` | 155 | 基色相(绿) |
| `hueSpread` | 46 | 流向带来的色相偏移范围(°) |
| `mouse` | `swirl` | `swirl` 漩涡 / `repel` 排斥 / `off` 关闭 |

引擎自动处理 DPR、resize、`prefers-reduced-motion`(画静态帧)、`document.hidden` 暂停。

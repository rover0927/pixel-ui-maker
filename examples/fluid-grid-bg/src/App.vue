<script setup>
import { reactive, ref, computed } from 'vue'
import GeekFluidGrid from './components/GeekFluidGrid.vue'

// 演示面板参数 —— 直接喂给 <GeekFluidGrid> 的 options，改动即实时生效
const settings = reactive({
  flowMode: 'noise',
  hue: 155,
  hueSpread: 46,
  flowSpeed: 0.06,
  flicker: 1.4,
  brightness: 1.0,
  mouse: 'swirl',
  cellSize: 10,
  gap: 2,
})

const themes = [
  { key: 'green', label: '数据绿', hue: 155 },
  { key: 'cyan', label: '科技青', hue: 185 },
  { key: 'magenta', label: '赛博洋红', hue: 320 },
  { key: 'teal', label: '松石流光', hue: 168 },
  { key: 'amber', label: '琥珀暖光', hue: 40 },
  { key: 'blue', label: '深海蓝', hue: 215 },
]
const flowModes = [
  { key: 'noise', label: '噪声场' },
  { key: 'wave', label: '波浪场' },
  { key: 'vortex', label: '涡流场' },
  { key: 'disturb', label: '干扰波' },
]
const mouseModes = [
  { key: 'swirl', label: '漩涡' },
  { key: 'repel', label: '排斥' },
  { key: 'off', label: '关闭' },
]

const activeTheme = ref('green')
const panelOpen = ref(true)
const copied = ref(false)
const stats = ref({ fps: 0, pixels: 0, cols: 0, rows: 0 })

// 一键把当前参数复制为 JSON —— 用户可直接粘贴回给 agent，按参数复现效果
async function copyParams() {
  const json = JSON.stringify(settings, null, 2)
  try {
    await navigator.clipboard.writeText(json)
  } catch {
    // 非安全上下文(非 https/localhost)fallback：临时 textarea + execCommand
    const ta = document.createElement('textarea')
    ta.value = json
    ta.style.position = 'fixed'
    ta.style.opacity = '0'
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    ta.remove()
  }
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}

// 干扰波模式：方块位置固定；颜色主题/呼吸频率可调，无流向色偏/鼠标交互
const isDisturb = computed(() => settings.flowMode === 'disturb')

// 整个 UI 强调色跟随流场基色相（干扰波固定双色，不联动）
const accent = computed(() => `hsl(${settings.hue} 90% 62%)`)
const gridLabel = computed(() =>
  isDisturb.value ? 'DISTURB' : `${stats.value.cols}×${stats.value.rows}`,
)

function applyTheme(t) {
  activeTheme.value = t.key
  settings.hue = t.hue
}

function reset() {
  settings.flowMode = 'noise'
  settings.hue = 155
  settings.hueSpread = 46
  settings.flowSpeed = 0.06
  settings.flicker = 1.4
  settings.brightness = 1.0
  settings.mouse = 'swirl'
  settings.cellSize = 10
  settings.gap = 2
  activeTheme.value = 'green'
}

function onStats(s) {
  stats.value = s
}
</script>

<template>
  <div class="page" :style="{ '--accent': accent }">
    <GeekFluidGrid :options="settings" :on-stats="onStats" />

    <header class="header">
      <h1>FLUID GRID BG · 流体网格像素背景</h1>
      <div class="sub">双引擎像素网格 · 流场驱动 · 颜色映射 · 呼吸闪烁</div>
      <div class="tags">
        <span class="tag">VUE 3 + VITE</span>
        <span class="tag">CANVAS 2D</span>
        <span class="tag">MOUSE 扰动</span>
      </div>
    </header>

    <div class="stats">
      PIXELS <b>{{ stats.pixels }}</b> · GRID <b>{{ gridLabel }}</b><br />
      FPS <b>{{ stats.fps }}</b> · MODE <b>{{ settings.flowMode }}</b>
    </div>

    <div v-if="!isDisturb" class="hint">⇄ 移动鼠标 → 扰动流场</div>
    <div v-else class="hint">✱ 干扰波 · 像素点阵 · 双场流动 · 呼吸 · 无鼠标交互</div>

    <section v-if="panelOpen" class="panel">
      <div class="panel__head" @click="panelOpen = false">
        CONTROL // 参数 <span class="caret">▾ 收起</span>
      </div>
      <div class="panel__body">
        <h3>颜色主题</h3>
        <div class="themes">
          <button
            v-for="t in themes"
            :key="t.key"
            class="theme-chip"
            :class="{ active: activeTheme === t.key }"
            :style="{ '--chip': `hsl(${t.hue} 90% 60%)` }"
            @click="applyTheme(t)"
          >{{ t.label }}</button>
        </div>

        <div class="row">
          <label>网格大小 <span class="val">{{ settings.cellSize }}px</span></label>
          <input v-model.number="settings.cellSize" type="range" min="4" max="24" step="1" />
        </div>
        <div class="row">
          <label>间隙 <span class="val">{{ settings.gap }}px</span></label>
          <input v-model.number="settings.gap" type="range" min="0" max="8" step="1" />
        </div>
        <div class="row">
          <label>流动速度 <span class="val">{{ settings.flowSpeed.toFixed(2) }}</span></label>
          <input v-model.number="settings.flowSpeed" type="range" min="0" max="0.3" step="0.005" />
        </div>
        <div class="row">
          <label>呼吸频率 <span class="val">{{ settings.flicker.toFixed(2) }}</span></label>
          <input v-model.number="settings.flicker" type="range" min="0" max="6" step="0.1" />
        </div>
        <div class="row">
          <label>亮度 <span class="val">{{ settings.brightness.toFixed(2) }}</span></label>
          <input v-model.number="settings.brightness" type="range" min="0.2" max="1.8" step="0.05" />
        </div>
        <div class="row" :class="{ disabled: isDisturb }">
          <label>流向色偏 <span class="val">±{{ (settings.hueSpread / 2).toFixed(0) }}°</span></label>
          <input v-model.number="settings.hueSpread" type="range" min="0" max="120" step="2" :disabled="isDisturb" />
        </div>

        <h3>流场模式</h3>
        <div class="row seg">
          <button
            v-for="m in flowModes"
            :key="m.key"
            :class="{ active: settings.flowMode === m.key }"
            @click="settings.flowMode = m.key"
          >{{ m.label }}</button>
        </div>
        <div v-if="isDisturb" class="disturb-note">
          ✱ 干扰波模式：统一大小的像素点阵，无干扰线扫过。双噪声场分层——
          亮度场驱动细腻光斑游走，颜色场驱动米白↔主色平滑渐变，叠加呼吸潮汐；
          色调低亮、柔和不突兀。可调：颜色主题、呼吸频率、流动速度、亮度、
          网格大小 / 间隙。
        </div>

        <h3>鼠标扰动</h3>
        <div class="row seg" :class="{ disabled: isDisturb }">
          <button
            v-for="m in mouseModes"
            :key="m.key"
            :class="{ active: settings.mouse === m.key }"
            :disabled="isDisturb"
            @click="settings.mouse = m.key"
          >{{ m.label }}</button>
        </div>

        <div class="panel__foot">
          <span class="foot-note">《流体网格指南》</span>
          <div class="foot-actions">
            <button
              class="btn geek-copy-params"
              :class="{ copied }"
              title="复制当前参数 JSON，可粘贴回给 agent 复现效果"
              @click="copyParams"
            >{{ copied ? '✓ 已复制' : '复制参数' }}</button>
            <button class="btn" @click="reset">重置</button>
          </div>
        </div>
      </div>
    </section>

    <button v-else class="gear" @click="panelOpen = true">⚙ 控制</button>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useFluidGrid } from '../composables/useFluidGrid'
import { useDisturbanceWave } from '../composables/useDisturbanceWave'

// geek-fluid-grid — 背景画布组件，根据 options.flowMode 选择渲染引擎：
//   'disturb'         → 引擎 B：固定像素点阵 + 双噪声场 + 呼吸潮汐（useDisturbanceWave）
//   其余(noise/wave/vortex) → 引擎 A：固定网格流体动画 + 鼠标扰动（useFluidGrid）
// 用法：
//   <GeekFluidGrid :options="{ flowMode: 'disturb', cellSize: 10 }" />
//   <GeekFluidGrid :options="settings" :on-stats="cb" />
// options 变化实时生效；onStats 每 ~0.4s 回调 { fps, pixels, cols, rows }。
const props = defineProps({
  options: { type: Object, default: () => ({}) },
  onStats: { type: Function, default: null },
})

const canvas = ref(null)
let ctrl = null
let current = '' // 当前挂载的引擎：'grid' | 'disturb'

function mount(mode) {
  const key = mode === 'disturb' ? 'disturb' : 'grid'
  if (key === current) return
  ctrl?.stop()
  ctrl = key === 'disturb'
    ? useDisturbanceWave(canvas, props.options).start()
    : useFluidGrid(canvas, props.options).start()
  if (props.onStats) ctrl.setOnStats(props.onStats)
  current = key
}

onMounted(() => mount(props.options?.flowMode))
onBeforeUnmount(() => ctrl?.stop())

watch(() => props.options?.flowMode, (m) => mount(m))
watch(() => props.options, (o) => ctrl?.setOptions(o), { deep: true })
watch(() => props.onStats, (fn) => ctrl?.setOnStats(fn))
</script>

<template>
  <canvas ref="canvas" class="fluid-grid" aria-hidden="true"></canvas>
</template>

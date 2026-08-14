<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useParticleBg } from '../composables/useParticleBg'

// geek-particle-bg — 背景像素粒子网络。用法：
//   <GeekParticleBg />                         默认：按屏幕面积自动算粒子数
//   <GeekParticleBg :count="120" :link-dist="140" />
// 粒子画在 hero 背景最底层，鼠标滑过粒子会被推开、最近的粒子连线到光标。
const props = defineProps({
  count: { type: Number, default: 0 },     // 0 = 按屏幕面积自动
  linkDist: { type: Number, default: 0 },  // 0 = 用引擎默认 120
  colors: { type: Array, default: null },  // null = cyber-geek 调色板
})

const canvas = ref(null)
let stop = null

onMounted(() => {
  const { start } = useParticleBg(canvas, {
    maxCount: props.count || undefined,
    linkDist: props.linkDist || undefined,
    colors: props.colors || undefined,
  })
  stop = start()
})

onBeforeUnmount(() => stop?.())
</script>

<template>
  <canvas ref="canvas" class="geek-particle-bg" aria-hidden="true"></canvas>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useTypewriter } from '../composables/useTypewriter'
import { useCrtRipple } from '../composables/useCrtRipple'
import GeekParticleBg from './GeekParticleBg.vue'

const subEl = ref(null)
let stopType = null
let stopRipple = null

const { type } = useTypewriter()
const { start } = useCrtRipple()

const subtitle = [
  '> BOOT SEQUENCE STARTED',
  '> ACCESS GRANTED · WELCOME TO THE GRID',
  '> FULLSTACK · UI · CYBERPUNK · OPEN SOURCE',
]

onMounted(() => {
  if (subEl.value) {
    stopType = type(subEl.value, subtitle, { speed: 42, linePause: 650, loop: true })
  }
  stopRipple = start()
})

onBeforeUnmount(() => {
  stopType?.()
  stopRipple?.()
})
</script>

<template>
  <section id="home" class="geek-hero">
    <!-- 背景像素粒子网络（geek-particle-bg，最底层 canvas：粒子漂浮 + 邻近连线 + 鼠标排斥）-->
    <GeekParticleBg />

    <div class="geek-hero__inner">
      <p class="geek-eyebrow">// 黑客 · 设计 · 全栈</p>
      <h1 class="geek-hero__title" data-text="CYBER_GEEK">CYBER_GEEK</h1>
      <p ref="subEl" class="geek-hero__sub"><span class="geek-typewriter__caret">▌</span></p>

      <div class="geek-hero__meta">
        <span>ROLE <b>FULLSTACK</b></span>
        <span>ZONE <b>NIGHT_CITY</b></span>
        <span>STATUS <b>ONLINE</b></span>
      </div>

      <div class="geek-screen geek-screen--ripple">
        <b>&gt; NODE</b> cyber_geek_main :: 0x7F0A<br />
        <b>&gt; ROLE</b> full-stack · ui · cyberpunk<br />
        <b>&gt; KERNEL</b> void_kernel 3.14 <em>// secure</em><br />
        <b>&gt; UPTIME</b> 1460d :: 11:37:52
      </div>
    </div>

    <div class="geek-hero__scrolltip">
      <span>scroll</span>
      <svg viewBox="0 0 50 50" aria-hidden="true">
        <polyline points="25,12 25,38" />
        <polyline points="15,28 25,38 35,28" />
      </svg>
    </div>
  </section>
</template>

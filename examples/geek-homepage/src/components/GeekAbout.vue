<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useTypewriter } from '../composables/useTypewriter'

const typed = ref(null)
let stop = null
const { type } = useTypewriter()

const lines = [
  '$ whoami',
  '  cyber_geek  —  fullstack designer & developer',
  '$ uname -a',
  '  void_kernel 3.14 x86_64 · open_source',
  '$ ls skills/',
  '  vue/  react/  node/  rust/  glsl/  ui/  motion/',
  '$ status',
  '  ONLINE  ·  open to collaboration',
]

onMounted(() => {
  if (typed.value) stop = type(typed.value, lines, { speed: 30, linePause: 240 })
})
onBeforeUnmount(() => stop?.())
</script>

<template>
  <section id="about" class="geek-section" v-reveal>
    <p class="geek-eyebrow">// ABOUT ME</p>
    <div class="geek-window corner">
      <div class="geek-window__title">
        <span>~</span> terminal — about
        <span>[×]</span>
      </div>
      <div class="geek-window__body">
        <pre class="geek-about__log">
          <code><span ref="typed"></span><span class="geek-typewriter__caret">▌</span></code>
        </pre>
      </div>
    </div>
  </section>
</template>

<style scoped>
.geek-about__log {
  margin: 0;
  font-family: var(--geek-font-mono);
  font-size: 14px;
  line-height: 1.9;
  color: var(--geek-color-teal);
  white-space: pre-wrap;
}
</style>

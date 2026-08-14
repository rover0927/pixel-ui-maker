<script setup>
const tags = [
  { name: 'Vue3', tone: 'cyan' },
  { name: 'React', tone: 'teal' },
  { name: 'Node', tone: 'blue' },
  { name: 'Rust', tone: 'amber' },
  { name: 'GLSL', tone: 'magenta' },
  { name: 'UI/Motion', tone: 'cyan' },
  { name: 'Pixel-Art', tone: 'magenta' },
  { name: 'Open-Source', tone: 'teal' },
]

const bars = [
  { name: 'FRONTEND / VUE', pct: 92 },
  { name: 'CREATIVE CODING', pct: 78 },
  { name: 'BACKEND / NODE', pct: 70 },
  { name: 'MOTION / GLSL', pct: 64 },
]
</script>

<template>
  <section id="skills" class="geek-section" v-reveal>
    <p class="geek-eyebrow">// SKILLS</p>

    <div class="geek-skills__tags">
      <span
        v-for="t in tags"
        :key="t.name"
        class="geek-tag"
        :class="`geek-tag--${t.tone}`"
      >{{ t.name }}</span>
    </div>

    <div class="geek-skills__bars">
      <div v-for="b in bars" :key="b.name" class="geek-skills__bar">
        <div class="geek-skills__bar-head">
          <span>{{ b.name }}</span>
          <span>{{ b.pct }}%</span>
        </div>
        <div class="geek-bar">
          <div class="geek-bar__fill" :style="{ width: `${b.pct}%` }"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<!-- 样式统一由 assets/geek-homepage.css 的 .geek-tag / .geek-bar 系列提供（风格锁定） -->

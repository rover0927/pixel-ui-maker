<script setup>
import GeekNav from './components/GeekNav.vue'
import GeekHero from './components/GeekHero.vue'
import GeekMarquee from './components/GeekMarquee.vue'
import GeekAbout from './components/GeekAbout.vue'
import GeekSkills from './components/GeekSkills.vue'
import GeekProjects from './components/GeekProjects.vue'
import GeekPhotos from './components/GeekPhotos.vue'
import GeekContact from './components/GeekContact.vue'
import GeekFooter from './components/GeekFooter.vue'

const strips = [
  { text: 'PUSH TO GRID', tone: 'cyan' },
  { text: 'WAKE UP IN THE MATRIX', tone: 'magenta' },
  { text: 'RUN THE NEON DECK', tone: 'amber' },
]
</script>

<template>
  <!-- 共享 CRT 水波纹滤镜定义 —— useCrtRipple.js 驱动 #geek-crt-ripple 内部节点 -->
  <svg
    class="geek-filter-defs"
    width="0"
    height="0"
    aria-hidden="true"
    focusable="false"
  >
    <defs>
      <filter id="geek-crt-ripple" x="-20%" y="-20%" width="140%" height="140%">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0 1"
          numOctaves="2"
          seed="7"
          stitchTiles="stitch"
          result="warp"
        />
        <feDisplacementMap
          in="SourceGraphic"
          in2="warp"
          scale="12"
          xChannelSelector="R"
          yChannelSelector="G"
        />
      </filter>
    </defs>
  </svg>

  <GeekNav />

  <main class="geek-main">
    <GeekHero />

    <GeekMarquee :text="strips[0].text" :tone="strips[0].tone" :count="6" />

    <GeekAbout />
    <GeekSkills />
    <GeekMarquee :text="strips[1].text" :tone="strips[1].tone" :count="6" />

    <GeekProjects />
    <GeekPhotos />
    <GeekMarquee :text="strips[2].text" :tone="strips[2].tone" :count="6" />

    <GeekContact />
  </main>

  <GeekFooter />
</template>

<style scoped>
/* 页面布局容器 —— 主题样式统一由 assets/geek-homepage.css 提供（风格锁定） */
.geek-main {
  position: relative;
  max-width: 1300px;
  margin: 0 auto;
  padding: 96px 32px 60px;
  box-sizing: border-box;
}

.geek-main > * {
  margin-bottom: 56px;
}
.geek-main > *:last-child {
  margin-bottom: 0;
}
</style>

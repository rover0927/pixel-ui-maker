<script setup>
const projects = [
  {
    year: '2026',
    title: 'NEON_DECK — 赛博终端 UI 套件',
    desc: '像素数据流风格组件库，含蒸馏动态效果（擦除按钮 / 像素画上浮 / 光带 / CRT 波纹）。',
    tags: ['Vue3', 'CSS', 'Motion'],
  },
  {
    year: '2025',
    title: 'VOID_KERNEL — WebGL 粒子系统',
    desc: 'GLSL 顶点/片元着色器驱动的霓虹粒子风暴，60fps，移动端降级。',
    tags: ['WebGL', 'GLSL', 'Rust'],
  },
  {
    year: '2024',
    title: 'GRID_RUNNER — 像素画生成器',
    desc: '把草图/字符画转成可部署的像素精灵与动画序列帧，配套 CLI。',
    tags: ['Pixel-Art', 'Node', 'CLI'],
  },
]
</script>

<template>
  <section id="projects" class="geek-section" v-reveal>
    <p class="geek-eyebrow">// PROJECTS</p>

    <div class="geek-timeline">
      <article
        v-for="p in projects"
        :key="p.title"
        class="geek-timeline__item"
      >
        <span class="geek-timeline__dot"></span>
        <div class="geek-card corner">
          <div class="geek-card__head">
            <h3>{{ p.title }}</h3>
            <span class="geek-card__year">{{ p.year }}</span>
          </div>
          <p class="geek-card__desc">{{ p.desc }}</p>
          <div class="geek-card__tags">
            <span
              v-for="t in p.tags"
              :key="t"
              class="geek-tag geek-tag--cyan"
            >{{ t }}</span>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.geek-card { padding: 24px; }
.geek-card__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}
.geek-card__head h3 { font-size: 18px; color: var(--geek-color-text); }
.geek-card__year { font-family: var(--geek-font-mono); font-size: 13px; letter-spacing: .1em; color: var(--geek-color-crimson); }
.geek-card__desc { color: var(--geek-color-text-dim); }
.geek-card__tags { display: flex; gap: 8px; flex-wrap: wrap; }
</style>

<script setup>
// 拍立得板的占位"照片"——霓虹像素 SVG 图，可换成真实图片
const photos = [
  {
    src: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'%3E%3Crect width='200' height='260' fill='%230a0f18'/%3E%3Crect x='20' y='20' width='160' height='160' fill='%2300f0ff' opacity='.85'/%3E%3Crect x='45' y='45' width='110' height='110' fill='%2305070c'/%3E%3Crect x='70' y='70' width='60' height='60' fill='%2300f0ff'/%3E%3Crect x='85' y='85' width='30' height='30' fill='%2305070c'/%3E%3C/svg%3E",
  },
  {
    src: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'%3E%3Crect width='200' height='260' fill='%230a0f18'/%3E%3Crect x='20' y='20' width='160' height='160' fill='%23ff2bd6' opacity='.85'/%3E%3Ccircle cx='100' cy='100' r='48' fill='%2305070c'/%3E%3Ccircle cx='100' cy='100' r='20' fill='%23ff2bd6'/%3E%3C/svg%3E",
  },
  {
    src: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'%3E%3Crect width='200' height='260' fill='%230a0f18'/%3E%3Crect x='20' y='20' width='160' height='160' fill='%2300ffd5' opacity='.85'/%3E%3Crect x='30' y='140' width='140' height='40' fill='%2305070c'/%3E%3Crect x='60' y='40' width='12' height='100' fill='%2305070c'/%3E%3Crect x='110' y='60' width='12' height='80' fill='%2305070c'/%3E%3C/svg%3E",
  },
  {
    src: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'%3E%3Crect width='200' height='260' fill='%230a0f18'/%3E%3Crect x='20' y='20' width='160' height='160' fill='%23ffd500' opacity='.85'/%3E%3Crect x='40' y='40' width='120' height='120' fill='%2305070c'/%3E%3Crect x='60' y='80' width='80' height='12' fill='%23ffd500'/%3E%3Crect x='60' y='110' width='56' height='12' fill='%23ffd500'/%3E%3C/svg%3E",
  },
  {
    src: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'%3E%3Crect width='200' height='260' fill='%230a0f18'/%3E%3Crect x='20' y='20' width='160' height='160' fill='%23e6f1ff' opacity='.85'/%3E%3Cpolygon points='100,50 140,130 60,130' fill='%2305070c'/%3E%3Crect x='88' y='100' width='24' height='30' fill='%23ff2bd6'/%3E%3C/svg%3E",
  },
]
</script>

<template>
  <section id="photos" class="geek-section" v-reveal>
    <p class="geek-eyebrow">// PHOTOS</p>

    <div class="geek-photos">
      <div
        v-for="(p, i) in photos"
        :key="i"
        class="geek-photos__plate"
        :class="`geek-photos__plate--${i + 1}`"
      >
        <img :src="p.src" alt="neon photo" />
      </div>
    </div>
  </section>
</template>

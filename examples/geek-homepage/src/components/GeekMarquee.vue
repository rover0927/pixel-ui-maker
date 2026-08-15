<script setup>
// geek-marquee — 四向滚动光带分割带
const props = defineProps({
  text: { type: String, default: '// SYSTEM ONLINE · ACCESS GRANTED' },
  count: { type: Number, default: 6 }, // per half-run; x2 duplicated for -50% loop
  tone: { type: String, default: 'cyan' }, // cyan | teal | blue | amber | magenta
})
</script>

<template>
  <div class="geek-marquee-strip">
    <div
      class="geek-marquee geek-marquee--x"
      :class="`geek-marquee--tone-${props.tone}`"
    >
      <div class="geek-marquee__track">
        <span
          v-for="n in count * 2"
          :key="n"
          class="geek-marquee__item"
        >
          <b>▸</b> {{ text }}
        </span>
      </div>
    </div>
  </div>
</template>

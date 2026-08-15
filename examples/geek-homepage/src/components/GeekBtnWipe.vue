<script setup>
// geek-btn-wipe — 双层擦除按钮
defineProps({
  label: { type: String, default: 'CONTACT' },
  type: { type: String, default: 'button' },
  size: { type: String, default: '' }, // '' | '--sm' | '--lg'
})
defineEmits(['click'])
</script>

<template>
  <button
    class="geek-btn-wipe"
    :class="size ? `geek-btn-wipe${size}` : null"
    :type="type"
    @click="$emit('click', $event)"
  >
    <span class="geek-btn-wipe__label">{{ label }}</span>
    <svg class="geek-btn-wipe__icon" viewBox="0 0 50 50" aria-hidden="true">
      <polyline points="12,25 38,25" />
      <polyline points="28,15 38,25 28,35" />
    </svg>
  </button>
</template>

<!-- 样式统一由 assets/geek-homepage.css 的 .geek-btn-wipe 系列提供（风格锁定） -->

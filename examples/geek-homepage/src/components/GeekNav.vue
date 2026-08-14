<script setup>
import { ref } from 'vue'
import GeekBtnWipe from './GeekBtnWipe.vue'

const open = ref(false)

const links = [
  { id: 'about', label: 'About' },
  { id: 'skills', label: 'Skills' },
  { id: 'projects', label: 'Projects' },
  { id: 'photos', label: 'Photos' },
  { id: 'contact', label: 'Contact' },
]

function go(id) {
  open.value = false
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <header class="geek-nav">
    <div class="geek-nav__logo" @click="go('home')">
      <span>//</span> CYBER_GEEK
    </div>

    <div class="geek-nav__right">
      <nav class="geek-nav__links">
        <a
          v-for="l in links"
          :key="l.id"
          class="geek-nav__link"
          :href="`#${l.id}`"
          @click.prevent="go(l.id)"
        >{{ l.label }}</a>
      </nav>

      <GeekBtnWipe label="CONTACT" size="--sm" @click="go('contact')" />

      <svg
        class="geek-nav__menuicon"
        :class="open ? 'geek-nav__menuicon--open' : 'geek-nav__menuicon--closed'"
        viewBox="0 0 50 50"
        @click="open = !open"
        aria-label="toggle menu"
      >
        <circle cx="25" cy="25" r="30" />
        <line x1="12" y1="25" x2="38" y2="25" />
        <line x1="12" y1="25" x2="38" y2="25" />
      </svg>
    </div>
  </header>

  <div class="geek-menu" :class="{ 'geek-menu--open': open }">
    <div>
      <a
        v-for="(l, i) in links"
        :key="l.id"
        class="geek-menu__link"
        :style="{ '--i': i }"
        :href="`#${l.id}`"
        @click.prevent="go(l.id)"
      >{{ l.label }}</a>
    </div>
  </div>
</template>

<!-- 样式统一由 assets/geek-homepage.css 的 .geek-nav / .geek-menu 系列提供（风格锁定） -->

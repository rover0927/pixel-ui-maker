import { createApp } from 'vue'
import App from './App.vue'
import './assets/geek-homepage.css'

const app = createApp(App)

// v-reveal — add .geek-reveal--in when the element enters the viewport
app.directive('reveal', {
  mounted(el, binding) {
    el.classList.add('geek-reveal')
    if (binding.modifiers.now) {
      el.classList.add('geek-reveal--in')
      return
    }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.classList.add('geek-reveal--in')
      return
    }
    const io = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        el.classList.add('geek-reveal--in')
        io.disconnect()
      }
    }, { threshold: 0.15 })
    io.observe(el)
  },
})

app.mount('#app')

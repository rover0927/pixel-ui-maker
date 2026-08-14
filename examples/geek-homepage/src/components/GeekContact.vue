<script setup>
import { reactive, ref } from 'vue'
import GeekBtnWipe from './GeekBtnWipe.vue'

const form = reactive({ name: '', email: '', msg: '' })
const sent = ref(false)

function submit() {
  sent.value = true
  form.name = ''
  form.email = ''
  form.msg = ''
  setTimeout(() => (sent.value = false), 2600)
}
</script>

<template>
  <section id="contact" class="geek-section" v-reveal>
    <p class="geek-eyebrow">// CONTACT</p>

    <div class="geek-contact">
      <form class="geek-contact__form corner" @submit.prevent="submit">
        <label class="geek-contact__label">
          <span>NAME</span>
          <input v-model="form.name" class="geek-contact__input" type="text" required />
        </label>
        <label class="geek-contact__label">
          <span>EMAIL</span>
          <input v-model="form.email" class="geek-contact__input" type="email" required />
        </label>
        <label class="geek-contact__label">
          <span>MESSAGE</span>
          <textarea v-model="form.msg" class="geek-contact__textarea" required></textarea>
        </label>

        <div style="display:flex;align-items:center;gap:16px;margin-top:8px;">
          <GeekBtnWipe label="TRANSMIT" type="submit" />
          <span v-if="sent" class="geek-contact__sent">// SIGNAL SENT ✓</span>
        </div>
      </form>

      <div class="geek-contact__side">
        <div class="geek-contact__line"><span>◆</span> NODE / 0x7F0A — NIGHT_CITY</div>
        <div class="geek-contact__line"><span>◆</span> MAIL&nbsp;&nbsp;<a href="mailto:hi@cybergeek.dev">hi@cybergeek.dev</a></div>
        <div class="geek-contact__line"><span>◆</span> CHAN&nbsp;&nbsp;<a href="#" @click.prevent>github.com/cyber-geek</a></div>
        <div class="geek-contact__line"><span>◆</span> UPLINK&nbsp;&nbsp;<a href="#" @click.prevent>@night_runner</a></div>
        <p style="color:var(--geek-color-text-mute);font-family:var(--geek-font-mono);font-size:13px;letter-spacing:.06em;">
          // encrypted channel — response within 24h
        </p>
      </div>
    </div>
  </section>
</template>

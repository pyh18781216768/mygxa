<template>
  <div class="page-shell">
    <div class="login-card">
      <div class="brand-block">
        <p class="eyebrow">Python + Vue + MySQL</p>
        <h1>账号登录</h1>
        <p class="description">
          使用手机号、密码、短信验证码和滑动验证完成登录。
        </p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <label>
          <span>手机号</span>
          <input v-model="form.phone" maxlength="11" placeholder="请输入 11 位手机号" />
        </label>

        <label>
          <span>密码</span>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入登录密码"
          />
        </label>

        <label>
          <span>滑动验证</span>
          <div class="slider-box">
            <input
              type="range"
              min="0"
              max="100"
              v-model="sliderValue"
              @change="handleSlider"
              :disabled="sliderPassed"
            />
            <strong :class="sliderPassed ? 'passed' : ''">
              {{ sliderPassed ? '验证通过' : '拖到最右侧完成验证' }}
            </strong>
          </div>
        </label>

        <label>
          <span>验证码</span>
          <div class="code-row">
            <input v-model="form.code" maxlength="6" placeholder="请输入 6 位验证码" />
            <button type="button" class="secondary" @click="sendCode" :disabled="sendingCode">
              {{ sendingCode ? '发送中...' : '发送验证码' }}
            </button>
          </div>
        </label>

        <button class="primary" type="submit" :disabled="submitting">
          {{ submitting ? '登录中...' : '立即登录' }}
        </button>
      </form>

      <div class="tips">
        <p>演示账号：13800138000</p>
        <p>演示密码：Password123</p>
        <p>滑动验证通过后可获取验证码，默认验证码：123456</p>
      </div>

      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const API_BASE = 'http://127.0.0.1:8000/api'
const sliderValue = ref(0)
const sliderPassed = ref(false)
const sendingCode = ref(false)
const submitting = ref(false)
const message = ref('')

const form = reactive({
  phone: '13800138000',
  password: 'Password123',
  code: ''
})

const sliderToken = () => (sliderPassed.value ? 'slide-pass' : '')

const handleSlider = () => {
  sliderPassed.value = Number(sliderValue.value) === 100
  if (!sliderPassed.value) {
    message.value = '请继续拖动到最右侧完成滑动验证'
  } else {
    message.value = '滑动验证通过，可以发送验证码'
  }
}

const sendCode = async () => {
  if (!sliderPassed.value) {
    message.value = '请先完成滑动验证'
    return
  }

  sendingCode.value = true
  message.value = ''
  try {
    const response = await fetch(`${API_BASE}/send-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: form.phone, slider_token: sliderToken() })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || '验证码发送失败')
    message.value = data.message
  } catch (error) {
    message.value = error.message
  } finally {
    sendingCode.value = false
  }
}

const handleLogin = async () => {
  submitting.value = true
  message.value = ''
  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: form.phone,
        password: form.password,
        code: form.code,
        slider_token: sliderToken()
      })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || '登录失败')
    message.value = `${data.message}，手机号：${data.phone}`
  } catch (error) {
    message.value = error.message
  } finally {
    submitting.value = false
  }
}
</script>

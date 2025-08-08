<template>
  <div class="space-y-8">
    <!-- 页面标题 -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-primary mb-4">
        🎯 API 演示页面
      </h1>
      <p class="text-lg text-base-content/70">
        测试与后端 API 的交互功能
      </p>
    </div>

    <!-- API 测试区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Hello World API -->
      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-secondary">
            👋 Hello World API
          </h2>
          <p class="text-base-content/70 mb-4">
            测试基础的 GET 请求
          </p>
          <button 
            @click="testHelloAPI" 
            class="btn btn-primary"
            :class="{ 'loading': helloLoading }"
            :disabled="helloLoading"
          >
            {{ helloLoading ? '请求中...' : '测试 Hello API' }}
          </button>
          <div v-if="helloResult" class="mt-4">
            <h3 class="font-semibold mb-2">响应结果：</h3>
            <div class="bg-base-100 p-4 rounded-lg">
              <pre class="text-sm">{{ JSON.stringify(helloResult, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Health Check API -->
      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-success">
            💚 健康检查 API
          </h2>
          <p class="text-base-content/70 mb-4">
            检查后端服务状态
          </p>
          <button 
            @click="testHealthAPI" 
            class="btn btn-success"
            :class="{ 'loading': healthLoading }"
            :disabled="healthLoading"
          >
            {{ healthLoading ? '检查中...' : '检查健康状态' }}
          </button>
          <div v-if="healthResult" class="mt-4">
            <h3 class="font-semibold mb-2">服务状态：</h3>
            <div class="badge" :class="healthResult.status === 'healthy' ? 'badge-success' : 'badge-error'">
              {{ healthResult.status }}
            </div>
          </div>
        </div>
      </div>

      <!-- Echo API -->
      <div class="card bg-base-200 shadow-xl lg:col-span-2">
        <div class="card-body">
          <h2 class="card-title text-accent">
            🔄 Echo API
          </h2>
          <p class="text-base-content/70 mb-4">
            测试 POST 请求，发送数据并接收回显
          </p>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">输入要发送的数据（JSON格式）：</span>
            </label>
            <textarea 
              v-model="echoInput"
              class="textarea textarea-bordered h-24" 
              placeholder='{"name": "测试", "value": 123}'
            ></textarea>
          </div>
          
          <button 
            @click="testEchoAPI" 
            class="btn btn-accent mt-4"
            :class="{ 'loading': echoLoading }"
            :disabled="echoLoading || !echoInput.trim()"
          >
            {{ echoLoading ? '发送中...' : '发送 Echo 请求' }}
          </button>
          
          <div v-if="echoResult" class="mt-4">
            <h3 class="font-semibold mb-2">响应结果：</h3>
            <div class="bg-base-100 p-4 rounded-lg">
              <pre class="text-sm">{{ JSON.stringify(echoResult, null, 2) }}</pre>
            </div>
          </div>
          
          <div v-if="echoError" class="alert alert-error mt-4">
            <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 15c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <span>{{ echoError }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 连接状态 -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">🔗 连接状态</h2>
        <div class="stats stats-vertical lg:stats-horizontal shadow">
          <div class="stat">
            <div class="stat-title">前端端口</div>
            <div class="stat-value text-primary">3000</div>
            <div class="stat-desc">Vite 开发服务器</div>
          </div>
          
          <div class="stat">
            <div class="stat-title">后端端口</div>
            <div class="stat-value text-secondary">8080</div>
            <div class="stat-desc">FastAPI 服务器</div>
          </div>
          
          <div class="stat">
            <div class="stat-title">API 代理</div>
            <div class="stat-value text-accent">/api</div>
            <div class="stat-desc">前端 → 后端</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// 响应式数据
const helloLoading = ref(false)
const helloResult = ref(null)

const healthLoading = ref(false)
const healthResult = ref(null)

const echoLoading = ref(false)
const echoInput = ref('{"name": "测试用户", "message": "Hello from Vue!"}')
const echoResult = ref(null)
const echoError = ref('')

// API 测试函数
const testHelloAPI = async () => {
  helloLoading.value = true
  try {
    const response = await axios.get('/api/demo/hello')
    helloResult.value = response.data
  } catch (error) {
    console.error('Hello API 请求失败:', error)
  } finally {
    helloLoading.value = false
  }
}

const testHealthAPI = async () => {
  healthLoading.value = true
  try {
    const response = await axios.get('/api/demo/health')
    healthResult.value = response.data
  } catch (error) {
    console.error('Health API 请求失败:', error)
  } finally {
    healthLoading.value = false
  }
}

const testEchoAPI = async () => {
  echoLoading.value = true
  echoError.value = ''
  try {
    // 尝试解析 JSON
    const data = JSON.parse(echoInput.value)
    const response = await axios.post('/api/demo/echo', data)
    echoResult.value = response.data
  } catch (error) {
    if (error instanceof SyntaxError) {
      echoError.value = 'JSON 格式错误，请检查输入数据'
    } else {
      echoError.value = 'API 请求失败'
      console.error('Echo API 请求失败:', error)
    }
  } finally {
    echoLoading.value = false
  }
}
</script>

<style scoped>
/* 演示页面特定样式 */
</style>

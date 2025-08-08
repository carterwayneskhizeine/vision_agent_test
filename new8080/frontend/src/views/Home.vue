<template>
  <div class="space-y-8">
    <!-- 欢迎区域 -->
    <div class="text-center">
      <h1 class="text-5xl font-bold text-primary mb-4">
        🚀 欢迎使用空白模板
      </h1>
      <p class="text-xl text-base-content/70 mb-8">
        基于 Vue 3 + FastAPI + DaisyUI 的现代化开发模板
      </p>
      <div class="flex gap-4 justify-center">
        <router-link to="/demo" class="btn btn-primary btn-lg">
          🎯 查看演示
        </router-link>
        <a href="http://localhost:8080/docs" target="_blank" class="btn btn-outline btn-lg">
          📚 API 文档
        </a>
      </div>
    </div>

    <!-- 特性介绍 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-primary">
            ⚡ 快速开发
          </h2>
          <p>使用 Vite 构建工具，热重载开发体验</p>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-secondary">
            🎨 美观UI
          </h2>
          <p>集成 DaisyUI 和 Tailwind CSS，现代化设计</p>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-accent">
            🔧 类型安全
          </h2>
          <p>TypeScript 支持，提供完整的类型检查</p>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-warning">
            🌐 现代后端
          </h2>
          <p>FastAPI 提供高性能的 RESTful API</p>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-error">
            📱 响应式
          </h2>
          <p>完美适配各种设备尺寸</p>
        </div>
      </div>

      <div class="card bg-base-200 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-success">
            🚀 易部署
          </h2>
          <p>一键构建和部署配置</p>
        </div>
      </div>
    </div>

    <!-- 技术栈 -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4">📋 技术栈</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold mb-2 text-primary">前端技术</h3>
            <ul class="space-y-1 text-base-content/80">
              <li>• Vue 3 - 渐进式JavaScript框架</li>
              <li>• Vite - 快速构建工具</li>
              <li>• TypeScript - 类型安全</li>
              <li>• DaisyUI - UI组件库</li>
              <li>• Tailwind CSS - 实用优先CSS</li>
              <li>• Vue Router - 路由管理</li>
              <li>• Pinia - 状态管理</li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-2 text-secondary">后端技术</h3>
            <ul class="space-y-1 text-base-content/80">
              <li>• FastAPI - 现代Python Web框架</li>
              <li>• Uvicorn - ASGI服务器</li>
              <li>• Pydantic - 数据验证</li>
              <li>• CORS - 跨域支持</li>
              <li>• 自动API文档生成</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速开始 -->
    <div class="card bg-gradient-to-r from-primary to-secondary text-primary-content shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4">🚀 快速开始</h2>
        <div class="space-y-2">
          <p><span class="font-semibold">1. 安装依赖：</span>npm install (前端) + pip install -r requirements.txt (后端)</p>
          <p><span class="font-semibold">2. 启动服务：</span>python start-dev.py</p>
          <p><span class="font-semibold">3. 访问应用：</span>http://localhost:3000</p>
          <p><span class="font-semibold">4. API文档：</span>http://localhost:8080/docs</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 主页逻辑
</script>

<style scoped>
/* 主页特定样式 */
</style>

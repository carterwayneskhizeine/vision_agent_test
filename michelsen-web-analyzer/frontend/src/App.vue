<template>
  <div class="min-h-screen bg-base-200">
    <!-- 导航栏 -->
    <div class="navbar bg-base-100 shadow-lg">
      <div class="navbar-start">
        <div class="dropdown">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16"></path>
            </svg>
          </div>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/analysis">分析结果</router-link></li>
          </ul>
        </div>
      </div>
      
      <div class="navbar-center">
        <router-link to="/" class="btn btn-ghost text-xl">
          🔬 迈克尔逊干涉实验 AI 分析系统
        </router-link>
      </div>
      
      <div class="navbar-end">
        <div class="navbar-center hidden lg:flex">
          <ul class="menu menu-horizontal px-1">
            <li><router-link to="/" class="btn btn-ghost">首页</router-link></li>
            <li><router-link to="/analysis" class="btn btn-ghost">分析结果</router-link></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <main class="container mx-auto px-4 py-8">
      <router-view />
    </main>
    
    <!-- 底部 -->
    <footer class="footer footer-center p-4 bg-base-300 text-base-content">
      <div>
        <p>© 2024 迈克尔逊干涉实验 AI 分析系统. 基于 AI 技术的实验教学分析工具.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 这里是 Vue 3 Composition API 的设置
</script>
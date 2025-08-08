<template>
  <div class="min-h-screen bg-base-100">
    <!-- 导航栏 -->
    <div class="navbar bg-base-200 shadow-lg">
      <div class="navbar-start">
        <div class="dropdown">
          <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </div>
          <ul class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
            <li><router-link to="/">首页</router-link></li>
            <li><router-link to="/demo">演示</router-link></li>
          </ul>
        </div>
        <router-link to="/" class="btn btn-ghost normal-case text-xl">
          🚀 空白模板
        </router-link>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li><router-link to="/" class="btn btn-ghost">首页</router-link></li>
          <li><router-link to="/demo" class="btn btn-ghost">演示</router-link></li>
        </ul>
      </div>
      <div class="navbar-end">
        <div class="dropdown dropdown-end">
          <div class="btn btn-circle btn-ghost">
            <div class="indicator">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <main class="container mx-auto px-4 py-8">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="footer footer-center p-10 bg-base-200 text-base-content">
      <aside>
        <p class="font-bold">
          空白项目模板 
          <br/>
          基于 Vue 3 + FastAPI 构建
        </p>
        <p>版本 1.0.0 - 端口 8080</p>
      </aside>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 这里可以添加全局逻辑
</script>

<style scoped>
/* 这里可以添加组件特定样式 */
</style>

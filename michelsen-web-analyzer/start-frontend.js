#!/usr/bin/env node
/**
 * 前端开发服务器启动脚本
 * 用于开发环境下启动 Vite 前端服务
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('\ud83d\ude80 启动迈克尔逊干涉实验 AI 分析前端服务...');

// 检查工作目录
const frontendDir = path.join(__dirname, 'frontend');
if (!fs.existsSync(frontendDir)) {
    console.error('\u274c 错误: 未找到 frontend 目录');
    process.exit(1);
}

// 检查 package.json
const packageJsonPath = path.join(frontendDir, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
    console.error('\u274c 错误: 未找到 package.json');
    process.exit(1);
}

// 进入 frontend 目录
process.chdir(frontendDir);

// 检查是否安装依赖
if (!fs.existsSync('node_modules')) {
    console.log('\u26a0\ufe0f  检测到未安装依赖，正在安装...');
    try {
        execSync('npm install', { stdio: 'inherit' });
    } catch (error) {
        console.error('\u274c 依赖安装失败:', error.message);
        process.exit(1);
    }
}

console.log('\u2705 依赖已安装');
console.log('\ud83c\udf10 正在启动服务器: http://localhost:3000');
console.log('\ud83c\udfa8 使用框架: Vue 3 + Vite + DaisyUI');
console.log('\u2699\ufe0f  开发模式: 已启用热重载');
console.log('\ud83d\uded1 停止服务: Ctrl+C');
console.log('-'.repeat(50));

// 启动 Vite 服务器
const viteProcess = spawn('npm', ['run', 'dev'], { 
    stdio: 'inherit',
    shell: true 
});

viteProcess.on('error', (error) => {
    console.error('\u274c 启动服务器失败:', error);
    process.exit(1);
});

viteProcess.on('close', (code) => {
    if (code !== 0) {
        console.error(`\u274c 服务器退出，退出码: ${code}`);
    } else {
        console.log('\ud83d\uded1 服务器已停止');
    }
});

// 处理中断信号
process.on('SIGINT', () => {
    console.log('\n\ud83d\uded1 正在停止服务器...');
    viteProcess.kill('SIGINT');
});
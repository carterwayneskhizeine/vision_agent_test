<template>
  <div class="space-y-8">
    <!-- 标题区域 -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-primary mb-4">
        📊 AI 分析结果
      </h1>
      <p class="text-lg text-base-content/70">
        迈克尔逊干涉实验步驤智能对比分析
      </p>
    </div>

    <!-- 分析统计信息 -->
    <div class="stats shadow w-full">
      <div class="stat">
        <div class="stat-figure text-primary">
          👨‍🏫
        </div>
        <div class="stat-title">老师示范步驤</div>
        <div class="stat-value text-primary">{{ teacherStepsCount }}</div>
        <div class="stat-desc">个标准步驤</div>
      </div>
      
      <div class="stat">
        <div class="stat-figure text-secondary">
          🎓
        </div>
        <div class="stat-title">学生操作步驤</div>
        <div class="stat-value text-secondary">{{ studentStepsCount }}</div>
        <div class="stat-desc">个识别步驤</div>
      </div>
      
      <div class="stat">
        <div class="stat-figure text-accent">
          🎯
        </div>
        <div class="stat-title">分析精度</div>
        <div class="stat-value text-accent">{{ averageConfidence }}%</div>
        <div class="stat-desc">平均置信度</div>
      </div>
    </div>

    <!-- 步驤对比区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 老师示范步驤 -->
      <div class="space-y-6">
        <h2 class="text-2xl font-bold text-primary flex items-center">
          👨‍🏫 老师示范步驤分析
        </h2>
        
        <div v-for="step in teacherSteps" :key="`teacher-${step.step_id}-${step.timestamp}`" class="step-card">
          <div class="card-body">
            <h3 class="card-title text-lg">
              步驤{{ step.step_id }}：{{ step.step_name }}
              <div class="badge badge-primary">t={{ step.timestamp }}s</div>
            </h3>
            
            <!-- 步驤截图 -->
            <div class="screenshot-container">
              <img 
                :src="getScreenshotUrl(step.screenshot_filename)" 
                :alt="step.step_name"
                class="step-screenshot"
                @click="openImageModal(getScreenshotUrl(step.screenshot_filename), step.step_name)"
              />
            </div>
            
            <!-- 步驤解释 -->
            <div class="space-y-2">
              <h4 class="font-semibold text-base-content">操作内容：</h4>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li v-for="action in step.description" :key="action" class="text-base-content/80">
                  {{ action }}
                </li>
              </ul>
              <div class="mt-3 p-3 bg-base-200 rounded-lg">
                <p class="text-sm">
                  <strong class="text-primary">AI 解读：</strong>
                  {{ step.explanation }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学生操作步驤 -->
      <div class="space-y-6">
        <h2 class="text-2xl font-bold text-secondary flex items-center">
          🎓 学生操作步驤分析
        </h2>
        
        <div v-for="step in studentSteps" :key="`student-${step.step_id}-${step.timestamp}`" class="step-card">
          <div class="card-body">
            <h3 class="card-title text-lg">
              步驤{{ step.step_id }}：{{ step.step_name }}
              <div class="badge badge-secondary">t={{ step.timestamp }}s</div>
              <div class="confidence-badge" :class="getConfidenceClass(step.confidence)">
                置信度: {{ (step.confidence * 100).toFixed(0) }}%
              </div>
            </h3>
            
            <!-- 步驤截图 -->
            <div class="screenshot-container">
              <img 
                :src="getScreenshotUrl(step.screenshot_filename)" 
                :alt="step.step_name"
                class="step-screenshot"
                @click="openImageModal(getScreenshotUrl(step.screenshot_filename), step.step_name)"
              />
            </div>
            
            <!-- 步驤解释 -->
            <div class="space-y-2">
              <h4 class="font-semibold text-base-content">操作内容：</h4>
              <ul class="list-disc list-inside space-y-1 text-sm">
                <li v-for="action in step.description" :key="action" class="text-base-content/80">
                  {{ action }}
                </li>
              </ul>
              <div class="mt-3 p-3 bg-base-200 rounded-lg">
                <p class="text-sm">
                  <strong class="text-secondary">AI 解读：</strong>
                  {{ step.explanation }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 重新分析按钮 -->
    <div class="text-center">
      <router-link to="/" class="btn btn-primary btn-lg">
        🔄 重新分析
      </router-link>
    </div>
    
    <!-- 图片放大模态框 -->
    <dialog id="image_modal" class="modal">
      <div class="modal-box max-w-4xl">
        <h3 class="font-bold text-lg mb-4">{{ selectedImageTitle }}</h3>
        <img :src="selectedImageUrl" :alt="selectedImageTitle" class="w-full h-auto" />
        <div class="modal-action">
          <form method="dialog">
            <button class="btn">关闭</button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 类型定义
interface StepData {
  step_id: number
  step_name: string
  timestamp: number
  time_str: string
  description: string[]
  explanation: string
  screenshot_filename: string
  confidence?: number
}

// 响应式数据
const teacherSteps = ref<StepData[]>([])
const studentSteps = ref<StepData[]>([])
const selectedImageUrl = ref('')
const selectedImageTitle = ref('')

// 计算属性
const teacherStepsCount = computed(() => teacherSteps.value.length)
const studentStepsCount = computed(() => studentSteps.value.length)
const averageConfidence = computed(() => {
  if (studentSteps.value.length === 0) return 0
  const total = studentSteps.value.reduce((sum, step) => sum + (step.confidence || 0), 0)
  return Math.round((total / studentSteps.value.length) * 100)
})

// 方法
const getScreenshotUrl = (filename: string) => {
  // TODO: 这里将从后端 API 获取截图 URL
  return `/api/screenshots/${filename}`
}

const getConfidenceClass = (confidence: number) => {
  if (confidence >= 0.8) return 'high'
  if (confidence >= 0.6) return 'medium'
  return 'low'
}

const openImageModal = (imageUrl: string, title: string) => {
  selectedImageUrl.value = imageUrl
  selectedImageTitle.value = title
  const modal = document.getElementById('image_modal') as HTMLDialogElement
  modal?.showModal()
}

const loadAnalysisResults = async () => {
  try {
    // TODO: 这里将从后端 API 获取分析结果
    // 模拟数据
    teacherSteps.value = [
      {
        step_id: 1,
        step_name: '迈克尔逊干涉仪初始设置',
        timestamp: 8,
        time_str: '00:08',
        description: ['安装氦氖激光器', '确保架间隙均匀', '准备光学元件'],
        explanation: '老师在8秒时执行: 迈克尔逊干涉仪初始设置',
        screenshot_filename: 'teacher_step_01_t8s.png'
      }
    ]
    
    studentSteps.value = [
      {
        step_id: 1,
        step_name: '迈克尔逊干涉仪初始设置',
        timestamp: 30,
        time_str: '00:30',
        description: ['准备和检查设备', '调整基础配置'],
        explanation: '学生在30秒时执行: 迈克尔逊干涉仪初始设置',
        screenshot_filename: 'student_step_01_t30s.png',
        confidence: 0.75
      }
    ]
    
  } catch (error) {
    console.error('加载分析结果失败:', error)
  }
}

// 生命周期
onMounted(() => {
  loadAnalysisResults()
})
</script>
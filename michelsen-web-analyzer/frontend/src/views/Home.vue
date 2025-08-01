<template>
  <div class="space-y-8">
    <!-- 标题区域 -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-primary mb-4">
        🔬 迈克尔逊干浉实验 AI 视频分析
      </h1>
      <p class="text-lg text-base-content/70">
        上传老师示范视频和学生实验视频，获得 AI 智能分析结果
      </p>
    </div>

    <!-- 视频上传区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 老师视频上传 -->
      <div class="upload-card">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-4">
            👨‍🏫 老师示范视频
            <div class="badge badge-primary">teacher.mp4</div>
          </h2>
          
          <!-- 上传区域 -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">请选择老师示范视频文件</span>
            </label>
            <input 
              type="file" 
              accept="video/mp4"
              @change="handleTeacherUpload"
              class="file-input file-input-bordered file-input-primary" 
            />
          </div>
          
          <!-- 视频预览 -->
          <div v-if="teacherVideoUrl" class="video-preview mt-4">
            <video 
              controls 
              class="w-full max-h-64 object-contain"
              :src="teacherVideoUrl">
              您的浏览器不支持视频播放
            </video>
          </div>
          
          <!-- 状态显示 -->
          <div v-if="teacherVideo" class="mt-4">
            <div class="alert alert-success">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>老师视频已上传：{{ teacherVideo.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 学生视频上传 -->
      <div class="upload-card">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-4">
            🎓 学生实验视频
            <div class="badge badge-secondary">student.mp4</div>
          </h2>
          
          <!-- 上传区域 -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">请选择学生实验视频文件</span>
            </label>
            <input 
              type="file" 
              accept="video/mp4"
              @change="handleStudentUpload"
              class="file-input file-input-bordered file-input-secondary" 
            />
          </div>
          
          <!-- 视频预览 -->
          <div v-if="studentVideoUrl" class="video-preview mt-4">
            <video 
              controls 
              class="w-full max-h-64 object-contain"
              :src="studentVideoUrl">
              您的浏览器不支持视频播放
            </video>
          </div>
          
          <!-- 状态显示 -->
          <div v-if="studentVideo" class="mt-4">
            <div class="alert alert-success">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>学生视频已上传：{{ studentVideo.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分析控制区域 -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body text-center">
        <h2 class="card-title justify-center text-2xl mb-4">
          🚀 AI 分析控制
        </h2>
        
        <!-- 分析选项 -->
        <div class="form-control mb-6">
          <label class="cursor-pointer label justify-center">
            <input 
              type="checkbox" 
              v-model="includeDeviceDetection" 
              class="checkbox checkbox-primary" 
            />
            <span class="label-text ml-2">包含设备检测 (108秒单帧)</span>
          </label>
        </div>
        
        <!-- 开始分析按钮 -->
        <div class="card-actions justify-center">
          <button 
            class="btn btn-primary btn-lg"
            :class="{ 'btn-disabled': !canStartAnalysis, 'loading': isAnalyzing }"
            :disabled="!canStartAnalysis || isAnalyzing"
            @click="startAnalysis">
            <span v-if="!isAnalyzing">🧠 开始 AI 实验步驤分析</span>
            <span v-else>正在分析中...</span>
          </button>
        </div>
        
        <!-- 分析进度 -->
        <div v-if="isAnalyzing" class="analysis-progress mt-6">
          <div class="mb-2">
            <span class="text-sm font-medium">分析进度: {{ analysisProgress }}%</span>
          </div>
          <progress class="progress progress-primary" :value="analysisProgress" max="100"></progress>
          <div class="mt-2 text-sm text-base-content/70">
            {{ currentAnalysisStep }}
          </div>
        </div>
        
        <!-- 提示信息 -->
        <div v-if="!canStartAnalysis" class="alert alert-warning mt-4">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
          <span>请先上传老师示范视频和学生实验视频</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// 响应式数据
const router = useRouter()
const teacherVideo = ref<File | null>(null)
const studentVideo = ref<File | null>(null)
const teacherVideoUrl = ref<string>('')
const studentVideoUrl = ref<string>('')
const includeDeviceDetection = ref(true)
const isAnalyzing = ref(false)
const analysisProgress = ref(0)
const currentAnalysisStep = ref('')

// 计算属性
const canStartAnalysis = computed(() => {
  return teacherVideo.value && studentVideo.value && !isAnalyzing.value
})

// 方法
const handleTeacherUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    teacherVideo.value = file
    teacherVideoUrl.value = URL.createObjectURL(file)
  }
}

const handleStudentUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    studentVideo.value = file
    studentVideoUrl.value = URL.createObjectURL(file)
  }
}

const startAnalysis = async () => {
  if (!canStartAnalysis.value) return
  
  isAnalyzing.value = true
  analysisProgress.value = 0
  currentAnalysisStep.value = '正在初始化分析...'
  
  try {
    // TODO: 这里将调用后端 API 进行分析
    // 模拟分析进度
    const steps = [
      '上传视频文件...',
      '提取关键帧...',
      'AI 分析老师示范步驤...',
      'AI 分析学生操作步驤...',
      '生成截图和解释...',
      '分析完成!'
    ]
    
    for (let i = 0; i < steps.length; i++) {
      currentAnalysisStep.value = steps[i]
      analysisProgress.value = ((i + 1) / steps.length) * 100
      await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟延迟
    }
    
    // 跳转到结果页面
    router.push('/analysis')
    
  } catch (error) {
    console.error('分析失败:', error)
    // TODO: 显示错误提示
  } finally {
    isAnalyzing.value = false
  }
}
</script>
<template>
  <div class="space-y-8">
    <!-- 标题区域 -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-primary mb-4">
        🧪 迈克尔逊干涉实验 AI 分析系统
      </h1>
      <p class="text-lg text-base-content/70">
        上传实验视频，AI 智能分析实验步骤并生成详细报告
      </p>
    </div>

    <!-- 视频上传区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- 老师示范视频上传 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-primary">
            👨‍🏫 老师示范视频
          </h2>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">选择老师示范视频文件</span>
            </label>
            <input 
              type="file" 
              accept="video/*" 
              class="file-input file-input-bordered file-input-primary" 
              @change="handleTeacherUpload"
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

      <!-- 学生实验视频上传 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-secondary">
            🎓 学生实验视频
          </h2>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">选择学生实验视频文件</span>
            </label>
            <input 
              type="file" 
              accept="video/*" 
              class="file-input file-input-bordered file-input-secondary" 
              @change="handleStudentUpload"
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
            <span v-if="!isAnalyzing">🧠 开始 AI 实验步骤分析</span>
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
    // 步骤1: 上传老师视频
    currentAnalysisStep.value = '上传老师示范视频...'
    analysisProgress.value = 10
    
    const teacherFormData = new FormData()
    teacherFormData.append('file', teacherVideo.value!)
    
    const teacherResponse = await fetch('/api/upload/teacher', {
      method: 'POST',
      body: teacherFormData
    })
    
    if (!teacherResponse.ok) {
      throw new Error('老师视频上传失败')
    }
    
    // 步骤2: 上传学生视频
    currentAnalysisStep.value = '上传学生实验视频...'
    analysisProgress.value = 20
    
    const studentFormData = new FormData()
    studentFormData.append('file', studentVideo.value!)
    
    const studentResponse = await fetch('/api/upload/student', {
      method: 'POST',
      body: studentFormData
    })
    
    if (!studentResponse.ok) {
      throw new Error('学生视频上传失败')
    }
    
    // 步骤3: 开始AI分析
    currentAnalysisStep.value = '启动AI分析引擎...'
    analysisProgress.value = 30
    
    const analysisResponse = await fetch('/api/analysis/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        include_device_detection: includeDeviceDetection.value
      })
    })
    
    if (!analysisResponse.ok) {
      throw new Error('AI分析启动失败')
    }
    
    const analysisResult = await analysisResponse.json()
    const analysisId = analysisResult.analysis_id
    
    // 步骤4: 轮询分析进度
    currentAnalysisStep.value = 'AI正在分析实验步骤...'
    
    let completed = false
    while (!completed) {
      await new Promise(resolve => setTimeout(resolve, 2000)) // 每2秒检查一次
      
      const progressResponse = await fetch(`/api/analysis/progress/${analysisId}`)
      if (!progressResponse.ok) {
        throw new Error('无法获取分析进度')
      }
      
      const progressData = await progressResponse.json()
      
      analysisProgress.value = Math.min(30 + progressData.progress * 0.7, 100)
      currentAnalysisStep.value = progressData.current_step || 'AI正在分析中...'
      
      if (progressData.status === 'completed') {
        completed = true
        analysisProgress.value = 100
        currentAnalysisStep.value = '分析完成！正在跳转到结果页面...'
      } else if (progressData.status === 'error') {
        throw new Error(progressData.error || '分析过程中出现错误')
      }
    }
    
    // 等待一下再跳转，让用户看到完成消息
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 跳转到结果页面
    router.push('/analysis')
    
  } catch (error) {
    console.error('分析失败:', error)
    alert(`AI分析失败: ${error.message}\n\n请检查：\n1. 后端服务是否正常运行\n2. 视频文件是否正确\n3. 网络连接是否稳定`)
    analysisProgress.value = 0
    currentAnalysisStep.value = ''
  } finally {
    isAnalyzing.value = false
  }
}
</script>

<style scoped>
.video-preview {
  @apply border-2 border-dashed border-base-300 rounded-lg p-4;
}

.analysis-progress {
  @apply w-full max-w-md mx-auto;
}

.btn.loading {
  @apply opacity-70;
}
</style>
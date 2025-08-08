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

    <!-- 没有数据时的提示 -->
    <div v-if="teacherStepsCount === 0 && studentStepsCount === 0" class="text-center py-16">
      <div class="text-6xl mb-4">🤖</div>
      <h2 class="text-2xl font-bold text-base-content mb-4">暂无分析结果</h2>
      <p class="text-base-content/70 mb-6">
        请先在主页上传视频并完成AI分析，然后再查看结果
      </p>
      <router-link to="/" class="btn btn-primary btn-lg">
        📹 返回上传页面
      </router-link>
    </div>

    <!-- 分析统计信息 -->
    <div v-else class="stats shadow w-full">
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
        
        <!-- 设备检测结果图片 -->
        <div v-if="detectionImageUrl" class="card bg-base-100 shadow-xl mb-6">
          <div class="card-body">
            <h3 class="card-title text-accent mb-4">
              🔍 学生实验设备检测结果 (108秒)
            </h3>
            <div class="screenshot-container">
              <img 
                :src="detectionImageUrl"
                alt="学生实验设备检测结果"
                class="step-screenshot cursor-pointer"
                @click="openImageModal(detectionImageUrl, '学生实验设备检测结果 (108秒)')"
                @error="handleImageError"
              />
            </div>
            <div class="mt-3 p-3 bg-accent/10 rounded-lg">
              <p class="text-sm">
                <strong class="text-accent">AI设备检测：</strong>
                {{ detectionResults ? `成功检测到 ${detectionResults.components_detected}/${detectionResults.total_components_to_detect} 个实验设备` : '正在加载设备检测结果...' }}
              </p>
            </div>
          </div>
        </div>
        
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

    <!-- 设备检测结果区域 -->
    <div v-if="detectionResults" class="space-y-6">
      <h2 class="text-2xl font-bold text-accent flex items-center">
        🔬 设备检测结果
      </h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 检测统计 -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h3 class="card-title text-accent">📊 检测统计</h3>
            <div class="stats stats-vertical shadow">
              <div class="stat">
                <div class="stat-title">总检测设备数</div>
                <div class="stat-value text-primary">{{ detectionResults.total_components_to_detect }}</div>
              </div>
              <div class="stat">
                <div class="stat-title">成功检测数</div>
                <div class="stat-value text-success">{{ detectionResults.components_detected }}</div>
              </div>
              <div class="stat">
                <div class="stat-title">检测成功率</div>
                <div class="stat-value text-accent">{{ (detectionResults.detection_rate * 100).toFixed(1) }}%</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 检测结果图片 -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h3 class="card-title text-accent">🖼️ 检测结果图</h3>
            <div class="screenshot-container">
              <img 
                :src="detectionImageUrl"
                alt="设备检测结果"
                class="step-screenshot cursor-pointer"
                @click="openImageModal(detectionImageUrl, '设备检测结果')"
                @error="handleImageError"
                v-if="detectionImageUrl"
              />
              <div v-else class="flex items-center justify-center h-48 bg-base-200 rounded-lg border-2 border-dashed border-base-300">
                <div class="text-center text-base-content/50">
                  <div class="text-4xl mb-2">🔍</div>
                  <p>设备检测结果图片加载中...</p>
                </div>
              </div>
            </div>
            <p class="text-sm text-base-content/70 mt-2">
              点击图片查看详细的设备检测标注结果
            </p>
          </div>
        </div>
      </div>
      
      <!-- 检测详情 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h3 class="card-title text-accent">🔍 检测详情</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            <div v-for="(detection, index) in detectionResults.detections" :key="index" 
                 class="card bg-base-200 shadow">
              <div class="card-body p-4">
                <h4 class="font-bold text-sm">{{ detection.name }}</h4>
                <div class="text-xs space-y-1">
                  <p><strong>置信度:</strong> {{ (detection.confidence * 100).toFixed(1) }}%</p>
                  <p><strong>检测方法:</strong> {{ detection.method }}</p>
                  <p><strong>位置:</strong> {{ formatBbox(detection.bbox) }}</p>
                </div>
                <div class="mt-2">
                  <div class="badge" :class="getConfidenceBadgeClass(detection.confidence)">
                    {{ getConfidenceLabel(detection.confidence) }}
                  </div>
                </div>
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

// 类型定义
interface DetectionResult {
  analysis_time: string
  source_video: string
  target_image: string
  total_components_to_detect: number
  components_detected: number
  detection_rate: number
  detections: Array<{
    name: string
    confidence: number
    bbox: number[]
    method: string
  }>
}

// 响应式数据
const teacherSteps = ref<StepData[]>([])
const studentSteps = ref<StepData[]>([])
const detectionResults = ref<DetectionResult | null>(null)
const detectionImageUrl = ref<string>('')
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
  return `/api/analysis/screenshots/${filename}`
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

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  console.warn('图片加载失败:', img.src)
  
  // 如果是检测结果图片加载失败，清空URL
  if (img.src.includes('detection_result.png')) {
    detectionImageUrl.value = ''
  }
}

const formatBbox = (bbox: number[]) => {
  const [x1, y1, x2, y2] = bbox
  return `(${x1}, ${y1}) - (${x2}, ${y2})`
}

const getConfidenceBadgeClass = (confidence: number) => {
  if (confidence >= 0.8) return 'badge-success'
  if (confidence >= 0.6) return 'badge-warning'
  return 'badge-error'
}

const getConfidenceLabel = (confidence: number) => {
  if (confidence >= 0.8) return '高'
  if (confidence >= 0.6) return '中'
  return '低'
}

const loadAnalysisResults = async () => {
  try {
    console.log('正在加载AI分析结果...')
    
    // 获取截图说明数据
    const screenshotResponse = await fetch('/api/analysis/reports/screenshot_explanations.json')
    if (!screenshotResponse.ok) {
      throw new Error(`截图数据加载失败: ${screenshotResponse.status}`)
    }
    const screenshotData = await screenshotResponse.json()
    console.log('截图数据:', screenshotData)
    
    // 获取完整分析报告
    const reportResponse = await fetch('/api/analysis/reports/experiment_steps_analysis.json')  
    if (!reportResponse.ok) {
      throw new Error(`分析报告加载失败: ${reportResponse.status}`)
    }
    const reportData = await reportResponse.json()
    console.log('分析报告:', reportData)
    
    // 解析老师步骤数据
    const teacherStepsData: StepData[] = []
    if (reportData.teacher_analysis && reportData.teacher_analysis.steps) {
      for (const step of reportData.teacher_analysis.steps) {
        const screenshotKey = `teacher_step_${step.step_id.toString().padStart(2, '0')}_t${step.timestamp}s.png`
        const screenshotInfo = screenshotData[screenshotKey]
        
        teacherStepsData.push({
          step_id: step.step_id,
          step_name: step.step_name,
          timestamp: step.timestamp,
          time_str: step.time_str,
          description: Array.isArray(step.description) ? step.description : [step.description],
          explanation: screenshotInfo ? screenshotInfo.explanation : `老师在${step.timestamp}秒时执行: ${step.step_name}`,
          screenshot_filename: screenshotKey
        })
      }
    }
    
    // 解析学生步骤数据
    const studentStepsData: StepData[] = []
    if (reportData.student_analysis && reportData.student_analysis.steps) {
      for (const step of reportData.student_analysis.steps) {
        const screenshotKey = `student_step_${step.step_id.toString().padStart(2, '0')}_t${step.timestamp}s.png`
        const screenshotInfo = screenshotData[screenshotKey]
        
        studentStepsData.push({
          step_id: step.step_id,
          step_name: step.step_name,
          timestamp: step.timestamp,
          time_str: step.time_str,
          description: Array.isArray(step.description) ? step.description : [step.description],
          explanation: screenshotInfo ? screenshotInfo.explanation : `学生在${step.timestamp}秒时执行: ${step.step_name}`,
          screenshot_filename: screenshotKey,
          confidence: step.confidence || 0.7
        })
      }
    }
    
    teacherSteps.value = teacherStepsData
    studentSteps.value = studentStepsData
    
    // 尝试加载设备检测结果
    try {
      const detectionResponse = await fetch('/api/analysis/reports/detection_report.json')
      if (detectionResponse.ok) {
        const detectionData = await detectionResponse.json()
        detectionResults.value = detectionData
        console.log('设备检测结果:', detectionData)
        
        // 检查设备检测图片是否存在
        try {
                          const imageResponse = await fetch('http://localhost:8080/static/images/detection_result.png', { method: 'HEAD' })
          if (imageResponse.ok) {
                              detectionImageUrl.value = 'http://localhost:8080/static/images/detection_result.png'
          }
        } catch (imageError) {
          console.log('设备检测图片不存在')
        }
      } else {
        console.log('设备检测结果不存在或加载失败')
      }
    } catch (detectionError) {
      console.log('设备检测结果加载失败:', detectionError)
    }
    
    console.log('加载完成:', {
      teacher: teacherStepsData.length,
      student: studentStepsData.length,
      detection: detectionResults.value ? detectionResults.value.components_detected : '无'
    })
    
  } catch (error) {
    console.error('加载分析结果失败:', error)
    // 显示错误提示
    alert(`加载分析结果失败: ${error.message}\n\n请确保：\n1. 后端服务正在运行\n2. 已完成AI分析\n3. 分析结果文件存在`)
  }
}

// 生命周期
onMounted(() => {
  loadAnalysisResults()
})
</script>

<style scoped>
.step-card {
  @apply card bg-base-100 shadow-xl border border-base-300;
}

.screenshot-container {
  @apply w-full flex justify-center mb-4;
}

.step-screenshot {
  @apply max-w-full h-auto rounded-lg border-2 border-base-300 cursor-pointer transition-all duration-200;
  max-height: 300px;
}

.step-screenshot:hover {
  @apply border-primary shadow-lg scale-105;
}

.confidence-badge {
  @apply badge badge-sm;
}

.confidence-badge.high {
  @apply badge-success;
}

.confidence-badge.medium {
  @apply badge-warning;
}

.confidence-badge.low {
  @apply badge-error;
}

/* 图片加载失败时的占位符 */
.step-screenshot[style*="display: none"] + .placeholder {
  @apply bg-base-200 rounded-lg border-2 border-dashed border-base-300 flex items-center justify-center text-base-content/50;
  height: 200px;
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .step-card {
    @apply mb-6;
  }
}
</style>
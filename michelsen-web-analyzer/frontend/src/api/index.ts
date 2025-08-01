import axios from 'axios'
import type {
  UploadResponse,
  UploadStatus,
  AnalysisStartResponse,
  AnalysisProgress,
  AnalysisResult,
  ApiError
} from '@/types/api'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API 请求错误:', error)
    return Promise.reject(error)
  }
)

// 上传 API
export const uploadApi = {
  // 上传老师视频
  uploadTeacher: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post<UploadResponse>('/upload/teacher', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // 上传学生视频
  uploadStudent: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post<UploadResponse>('/upload/student', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // 获取上传状态
  getStatus: async (): Promise<UploadStatus> => {
    const response = await api.get<UploadStatus>('/upload/status')
    return response.data
  },

  // 获取视频预览 URL
  getVideoUrl: (videoType: 'teacher' | 'student'): string => {
    return `/api/upload/videos/${videoType}`
  },
}

// 分析 API
export const analysisApi = {
  // 开始分析
  start: async (includeDeviceDetection: boolean = true): Promise<AnalysisStartResponse> => {
    const response = await api.post<AnalysisStartResponse>('/analysis/start', null, {
      params: {
        include_device_detection: includeDeviceDetection,
      },
    })
    return response.data
  },

  // 获取分析进度
  getProgress: async (analysisId: string): Promise<AnalysisProgress> => {
    const response = await api.get<AnalysisProgress>(`/analysis/progress/${analysisId}`)
    return response.data
  },

  // 获取分析结果
  getResults: async (analysisId: string): Promise<AnalysisResult> => {
    const response = await api.get<AnalysisResult>(`/analysis/results/${analysisId}`)
    return response.data
  },

  // 获取截图 URL
  getScreenshotUrl: (filename: string): string => {
    return `/api/analysis/screenshots/${filename}`
  },

  // 获取分析列表
  getList: async () => {
    const response = await api.get('/analysis/list')
    return response.data
  },

  // 清空分析
  clear: async () => {
    const response = await api.delete('/analysis/clear')
    return response.data
  },
}

// 错误处理工具
export const handleApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    const apiError = error.response?.data as ApiError
    return apiError?.detail || error.message || '未知错误'
  }
  return error.message || '未知错误'
}

export default api
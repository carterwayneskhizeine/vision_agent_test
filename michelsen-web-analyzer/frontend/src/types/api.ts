// API 类型定义

// 上传响应
export interface UploadResponse {
  success: boolean;
  message: string;
  filename: string;
  size: number;
  preview_url: string;
}

// 上传状态
export interface UploadStatus {
  teacher_uploaded: boolean;
  student_uploaded: boolean;
  can_analyze: boolean;
  files: {
    teacher: FileInfo | null;
    student: FileInfo | null;
  };
}

export interface FileInfo {
  filename: string;
  filepath: string;
  size: number;
}

// 分析开始响应
export interface AnalysisStartResponse {
  success: boolean;
  analysis_id: string;
  message: string;
}

// 分析进度
export interface AnalysisProgress {
  status: 'running' | 'completed' | 'error';
  progress: number;
  current_step: string;
  include_device_detection: boolean;
  created_at: string;
  error?: string;
}

// 步驤数据
export interface StepData {
  step_id: number;
  step_name: string;
  timestamp: number;
  time_str: string;
  description: string[];
  formatted_output: string;
  confidence?: number;
}

// 老师分析结果
export interface TeacherAnalysis {
  video_type: '老师示范';
  total_steps_identified: number;
  analysis_summary: string;
  steps: StepData[];
}

// 学生分析结果
export interface StudentAnalysis {
  video_type: '学生操作';
  total_steps_identified: number;
  analysis_summary: string;
  steps: (StepData & { confidence: number })[];
}

// 截图解释
export interface ScreenshotExplanation {
  type: '老师示范' | '学生操作';
  step_id: number;
  step_name: string;
  timestamp: number;
  time_str: string;
  description: string[];
  explanation: string;
  confidence?: number;
}

// 完整分析结果
export interface AnalysisResult {
  analysis_time: string;
  analysis_type: string;
  videos_analyzed: {
    teacher_video: string;
    student_video: string;
  };
  teacher_analysis: TeacherAnalysis;
  student_analysis: StudentAnalysis;
  screenshot_explanations: Record<string, ScreenshotExplanation>;
  output_format_example: {
    description: string;
    format: string;
  };
  device_detection?: {
    enabled: boolean;
    detection_rate: number;
    components_detected: number;
  };
}

// API 错误响应
export interface ApiError {
  detail: string;
}
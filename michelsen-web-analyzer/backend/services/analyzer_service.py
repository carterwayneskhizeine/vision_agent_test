"""
AI分析服务类
封装实验分析核心逻辑
"""

import os
import json
import shutil
import asyncio  
import sys
from typing import Dict, Any, Optional, Callable

# 添加analyzer路径到sys.path
analyzer_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analyzer')
if analyzer_path not in sys.path:
    sys.path.insert(0, analyzer_path)

from experiment_analyzer_prototype import MichelsonInterferometerAnalyzer

class AnalyzerService:
    """实验分析服务"""
    
    def __init__(self, upload_dir: str, static_dir: str):
        self.upload_dir = upload_dir
        self.static_dir = static_dir
        self.analyzer = MichelsonInterferometerAnalyzer()
    
    async def analyze_videos(
        self, 
        teacher_video_path: str, 
        student_video_path: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        分析老师和学生视频
        
        Args:
            teacher_video_path: 老师视频文件路径
            student_video_path: 学生视频文件路径
            progress_callback: 进度回调函数
            
        Returns:
            分析结果字典
        """
        
        if progress_callback:
            progress_callback("开始AI分析...")
        
        try:
            # 调用完整的分析逻辑
            result = await self._run_full_analyzer(
                teacher_video_path, 
                student_video_path, 
                progress_callback
            )
            
            # 移动生成的截图和文件到静态目录
            await self._move_results_to_static()
            
            if progress_callback:
                progress_callback("分析完成")
                
            return result
            
        except Exception as e:
            print(f"分析过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            
            if progress_callback:
                progress_callback(f"分析失败: {str(e)}")
            
            # 返回错误结果
            return self._get_error_result(str(e))
    
    async def _run_full_analyzer(
        self, 
        teacher_path: str, 
        student_path: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """运行完整的分析逻辑（基于原始experiment_analyzer_prototype.py）"""
        
        # 设置工作目录为上传目录
        original_cwd = os.getcwd()
        os.chdir(self.upload_dir)
        
        try:
            # 检查必需文件是否存在
            if not os.path.exists('teacher.mp4'):
                raise FileNotFoundError("teacher.mp4 文件不存在")
            if not os.path.exists('student.mp4'):
                raise FileNotFoundError("student.mp4 文件不存在")
            
            if progress_callback:
                progress_callback("分析老师示范视频...")
            
            # 1. 分析老师视频步骤
            teacher_analysis = self.analyzer.analyze_video_steps('teacher.mp4', 'teacher', interval=30)
            
            if progress_callback:
                progress_callback("分析学生实验视频...")
            
            # 2. 分析学生视频步骤
            student_analysis = self.analyzer.analyze_video_steps('student.mp4', 'student', interval=30)
            
            if progress_callback:
                progress_callback("保存步骤截图和解释...")
            
            # 3. 保存截图和解释
            screenshot_explanations = self.analyzer.save_simple_analysis_screenshots(
                teacher_analysis, 
                student_analysis, 
                'step_analysis_output'
            )
            
            if progress_callback:
                progress_callback("生成完整分析报告...")
            
            # 4. 生成完整的分析报告
            analysis_report = self.analyzer.generate_simple_analysis_report(
                teacher_analysis, 
                student_analysis, 
                screenshot_explanations,
                'experiment_steps_analysis.json'
            )
            
            # 检查是否有part文件，如果有则执行设备检测
            has_part_files = any(os.path.exists(f'part{i}.png') for i in range(1, 7))
            if has_part_files:
                if progress_callback:
                    progress_callback("执行设备检测...")
                
                # 5. 复制part文件到上传目录（如果还没有的话）
                await self._copy_part_files()
                
                # 6. 执行单帧设备检测（基于108秒）
                from experiment_analyzer_prototype import extract_frame_at_time
                
                # 提取108秒的帧
                target_frame = extract_frame_at_time('student.mp4', time_seconds=108.0, output_path='Identify_target.png')
                
                # 转换为RGB格式用于分析
                import cv2
                target_frame_rgb = cv2.cvtColor(target_frame, cv2.COLOR_BGR2RGB)
                
                # 执行设备检测
                equipment_detections = self.analyzer.detect_equipment_in_frame(target_frame_rgb, min_confidence=0.25)
                
                if equipment_detections:
                    # 在原图上绘制检测结果
                    annotated_frame = self.analyzer.draw_detections_on_frame(target_frame_rgb, equipment_detections)
                    
                    # 保存标注后的图片
                    annotated_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
                    cv2.imwrite('detection_result.png', annotated_bgr)
                    
                    # 生成设备检测报告
                    detection_report = {
                        'analysis_time': analysis_report.get('analysis_time'),
                        'source_video': 'student.mp4',  
                        'target_image': 'Identify_target.png',
                        'total_components_to_detect': 7,
                        'components_detected': len(equipment_detections),
                        'detection_rate': len(equipment_detections) / 7,
                        'detections': [
                            {
                                'name': det['name'],
                                'confidence': det['confidence'],
                                'bbox': det['bbox'],
                                'method': det['method']
                            }
                            for det in equipment_detections
                        ]
                    }
                    
                    with open('detection_report.json', 'w', encoding='utf-8') as f:
                        json.dump(detection_report, f, ensure_ascii=False, indent=2)
                    
                    # 将设备检测结果添加到主报告中
                    analysis_report['equipment_detection'] = detection_report
            
            return analysis_report
            
        finally:
            # 恢复原始工作目录
            os.chdir(original_cwd)
    
    async def _copy_part_files(self):
        """复制part文件到上传目录"""
        # 检查是否需要从web目录复制part文件
        web_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.upload_dir))), 'web')
        
        for i in range(1, 8):  # part1.png to part7.png
            part_file = f'part{i}.png'
            upload_part_path = os.path.join(self.upload_dir, part_file)
            web_part_path = os.path.join(web_dir, part_file)
            
            # 如果上传目录没有这个文件，但web目录有，则复制过来
            if not os.path.exists(upload_part_path) and os.path.exists(web_part_path):
                shutil.copy2(web_part_path, upload_part_path)
                print(f"复制了 {part_file} 到上传目录")
    
    async def _move_results_to_static(self):
        """移动生成的结果文件到静态文件目录"""
        # 创建静态文件子目录
        static_screenshots_dir = os.path.join(self.static_dir, 'screenshots')
        static_reports_dir = os.path.join(self.static_dir, 'reports')
        static_images_dir = os.path.join(self.static_dir, 'images')
        
        os.makedirs(static_screenshots_dir, exist_ok=True)
        os.makedirs(static_reports_dir, exist_ok=True)  
        os.makedirs(static_images_dir, exist_ok=True)
        
        # 1. 移动步骤分析截图
        screenshots_dir = os.path.join(self.upload_dir, 'step_analysis_output')
        if os.path.exists(screenshots_dir):
            for filename in os.listdir(screenshots_dir):
                if filename.endswith('.png'):
                    src = os.path.join(screenshots_dir, filename)
                    dst = os.path.join(static_screenshots_dir, filename)
                    
                    if os.path.exists(dst):
                        os.remove(dst)
                    shutil.move(src, dst)
        
        # 2. 移动JSON报告文件
        report_files = [
            'experiment_steps_analysis.json',
            'detection_report.json',
            'screenshot_explanations.json'
        ]
        
        for report_file in report_files:
            src_path = os.path.join(self.upload_dir, report_file)
            if os.path.exists(src_path):
                dst_path = os.path.join(static_reports_dir, report_file)
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                shutil.move(src_path, dst_path)
        
        # 3. 移动检测相关图片
        image_files = [
            'Identify_target.png',
            'detection_result.png'
        ]
        
        for image_file in image_files:
            src_path = os.path.join(self.upload_dir, image_file)
            if os.path.exists(src_path):
                dst_path = os.path.join(static_images_dir, image_file)
                if os.path.exists(dst_path):
                    os.remove(dst_path)
                shutil.move(src_path, dst_path)
        
        # 4. 移动screenshot_explanations.json（可能在step_analysis_output目录中）
        screenshots_explanations_path = os.path.join(self.upload_dir, 'step_analysis_output', 'screenshot_explanations.json')
        if os.path.exists(screenshots_explanations_path):
            dst_path = os.path.join(static_reports_dir, 'screenshot_explanations.json')
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.move(screenshots_explanations_path, dst_path)
    
    def _get_error_result(self, error_message: str) -> Dict[str, Any]:
        """获取错误结果"""
        return {
            'analysis_time': '2024-01-01 12:00:00',
            'analysis_type': '实验步骤AI分析（老师示范 + 学生操作）',
            'videos_analyzed': {
                'teacher_video': 'teacher.mp4',
                'student_video': 'student.mp4'
            },
            'teacher_analysis': {
                'video_type': '老师示范',
                'total_steps_identified': 0,
                'analysis_summary': 'LGS-7A精密干涉仪实验步骤 - 老师示范',
                'steps': []
            },
            'student_analysis': {
                'video_type': '学生操作',
                'total_steps_identified': 0,
                'analysis_summary': 'LGS-7A精密干涉仪实验步骤 - 学生操作',
                'steps': []
            },
            'screenshot_explanations': {},
            'error': f'分析过程中出现错误: {error_message}',
            'success': False
        }
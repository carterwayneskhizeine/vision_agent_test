#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迈克尔逊干涉实验AI分析原型
整合视频分析和设备检测功能，用于教学评估

基于现有的video_test.py和imagetest_batch.py代码
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import time
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any, Optional, Tuple

# 设置matplotlib支持中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class MichelsonInterferometerAnalyzer:
    """迈克尔逊干涉仪实验分析器"""
    
    def __init__(self):
        """初始化分析器"""
        # 预定义的教师实验步骤（标准流程）
        self.teacher_steps = [
            {
                "step_id": 1,
                "name": "迈克尔逊干涉仪初始设置",
                "start_time": 8,
                "duration": 17,
                "key_actions": ["安装氦氖激光器", "确保架间隙均匀", "准备光学元件"],
                "required_equipment": ["氦氖激光器", "干涉仪框架"],
                "success_criteria": ["激光器正确安装", "框架水平稳定"]
            },
            {
                "step_id": 2,
                "name": "激光器对准和调节",
                "start_time": 25,
                "duration": 20,
                "key_actions": ["调节激光器位置", "调节光束通过分束器", "使光点重合"],
                "required_equipment": ["氦氖激光器", "分束器和补偿板", "二合一观察屏"],
                "success_criteria": ["光束对准", "两个光点重合"]
            },
            {
                "step_id": 3,
                "name": "获得干涉条纹",
                "start_time": 45,
                "duration": 15,
                "key_actions": ["加入扩束器", "调节动镜手钮", "获得干涉条纹"],
                "required_equipment": ["扩束器", "动镜", "精密测微头"],
                "success_criteria": ["出现清晰干涉条纹", "条纹位于中心"]
            },
            {
                "step_id": 4,
                "name": "观察等倾干涉图",
                "start_time": 60,
                "duration": 15,
                "key_actions": ["转动精密测微头", "调节测微头", "观察圆形干涉环"],
                "required_equipment": ["精密测微头", "二合一观察屏"],
                "success_criteria": ["出现圆形干涉环", "环心在屏中央"]
            },
            {
                "step_id": 5,
                "name": "精密测量过程",
                "start_time": 75,
                "duration": 17,
                "key_actions": ["记录测微头读数", "旋转测微螺旋", "计数干涉环变化"],
                "required_equipment": ["精密测微头"],
                "success_criteria": ["准确记录读数", "正确计数环数"]
            },
            {
                "step_id": 6,
                "name": "法布里-珀罗干涉设置",
                "start_time": 92,
                "duration": 22,
                "key_actions": ["取下分束器和补偿板", "安装镀膜面", "调节镜面间隙"],
                "required_equipment": ["定镜", "动镜"],
                "success_criteria": ["正确移除部件", "镜面间隙合适"]
            }
        ]
        
        # 设备映射（基于imagetest_batch.py）
        self.equipment_mapping = {
            'helium_neon_laser': '氦氖激光器',
            'beam_splitter': '分束器和补偿板',
            'moving_mirror': '动镜',
            'fixed_mirror': '定镜',
            'micrometer_head': '精密测微头',
            'beam_expander': '扩束器',
            'observation_screen': '二合一观察屏'
        }
        
        # 检测颜色
        self.colors = [
            (0, 0, 255),    # 红色
            (0, 255, 0),    # 绿色
            (255, 0, 0),    # 蓝色
            (0, 255, 255),  # 黄色
            (255, 255, 0),  # 青色
            (128, 0, 128),  # 紫色
            (255, 165, 0)   # 橙色
        ]

    def extract_key_frames(self, video_path: str, interval: int = 15) -> List[Dict]:
        """提取视频关键帧"""
        print(f"正在分析视频: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"视频信息: {total_frames} 帧, {fps:.2f} FPS, 时长: {timedelta(seconds=int(duration))}")
        
        key_frames = []
        timestamps = list(range(0, int(duration), interval))
        
        for timestamp in timestamps:
            frame_number = int(timestamp * fps)
            if frame_number >= total_frames:
                continue
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if ret:
                key_frames.append({
                    'timestamp': timestamp,
                    'frame_number': frame_number,
                    'frame': cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    'analysis': None
                })
        
        cap.release()
        return key_frames

    def detect_equipment_in_frame(self, frame: np.ndarray) -> List[Dict]:
        """在帧中检测实验设备（简化版本）"""
        # 这里是简化的设备检测逻辑
        # 实际应用中会使用更复杂的计算机视觉算法
        
        detections = []
        height, width = frame.shape[:2]
        
        # 模拟设备检测结果
        # 在实际应用中，这里会调用imagetest_batch.py中的检测函数
        mock_detections = [
            {'name': '氦氖激光器', 'bbox': (int(0.1*width), int(0.3*height), int(0.3*width), int(0.5*height)), 'confidence': 0.85},
            {'name': '分束器和补偿板', 'bbox': (int(0.4*width), int(0.4*height), int(0.6*width), int(0.6*height)), 'confidence': 0.78},
            {'name': '动镜', 'bbox': (int(0.7*width), int(0.2*height), int(0.9*width), int(0.4*height)), 'confidence': 0.92},
        ]
        
        return mock_detections

    def identify_experiment_step(self, frame: np.ndarray, timestamp: int, equipment_detections: List[Dict]) -> Dict:
        """识别当前实验步骤"""
        # 基于时间和检测到的设备推断当前步骤
        current_step = None
        confidence = 0.0
        
        for step in self.teacher_steps:
            if step['start_time'] <= timestamp <= step['start_time'] + step['duration']:
                current_step = step
                
                # 检查是否有必需的设备
                detected_equipment = [det['name'] for det in equipment_detections]
                required_count = len(step['required_equipment'])
                detected_count = len([eq for eq in step['required_equipment'] if eq in detected_equipment])
                
                confidence = detected_count / required_count if required_count > 0 else 0.5
                break
        
        if current_step is None:
            # 如果没有匹配的时间段，基于设备推测
            current_step = {
                "step_id": 0,
                "name": "未识别步骤",
                "start_time": timestamp,
                "duration": 0,
                "key_actions": ["未知操作"],
                "required_equipment": [],
                "success_criteria": []
            }
            confidence = 0.3
        
        return {
            'step': current_step,
            'confidence': confidence,
            'detected_equipment': equipment_detections,
            'timestamp': timestamp
        }

    def analyze_video(self, video_path: str, video_type: str = 'student') -> Dict:
        """分析视频的完整流程"""
        print(f"\n开始分析{video_type}视频...")
        
        # 提取关键帧
        key_frames = self.extract_key_frames(video_path)
        
        # 分析每一帧
        analysis_results = []
        for i, frame_data in enumerate(key_frames):
            print(f"分析第 {i+1}/{len(key_frames)} 帧 (t={frame_data['timestamp']}s)")
            
            # 设备检测
            equipment_detections = self.detect_equipment_in_frame(frame_data['frame'])
            
            # 步骤识别
            step_analysis = self.identify_experiment_step(
                frame_data['frame'], 
                frame_data['timestamp'], 
                equipment_detections
            )
            
            frame_data['analysis'] = step_analysis
            analysis_results.append(frame_data)
        
        return {
            'video_path': video_path,
            'video_type': video_type,
            'total_frames_analyzed': len(analysis_results),
            'key_frames': analysis_results,
            'steps_detected': list(set([frame['analysis']['step']['step_id'] for frame in analysis_results]))
        }

    def compare_student_with_teacher(self, student_analysis: Dict, teacher_analysis: Dict = None) -> Dict:
        """对比学生和教师的实验步骤"""
        print("\n开始对比分析...")
        
        student_frames = student_analysis['key_frames']
        comparison_results = []
        issues_found = []
        
        # 分析每个学生帧
        for frame_data in student_frames:
            student_step = frame_data['analysis']['step']
            timestamp = frame_data['timestamp']
            
            # 找到对应的教师步骤
            expected_step = None
            for teacher_step in self.teacher_steps:
                if teacher_step['start_time'] <= timestamp <= teacher_step['start_time'] + teacher_step['duration']:
                    expected_step = teacher_step
                    break
            
            # 对比分析
            if expected_step is None:
                issue_type = "时间偏差"
                issue_description = f"时间点 {timestamp}s 没有对应的标准步骤"
                is_correct = False
            elif student_step['step_id'] != expected_step['step_id']:
                issue_type = "步骤错误"
                issue_description = f"应该执行 '{expected_step['name']}'，但检测到 '{student_step['name']}'"
                is_correct = False
            else:
                issue_type = "正确"
                issue_description = f"正确执行了 '{student_step['name']}'"
                is_correct = True
            
            comparison_result = {
                'timestamp': timestamp,
                'frame': frame_data['frame'],
                'student_step': student_step,
                'expected_step': expected_step,
                'is_correct': is_correct,
                'issue_type': issue_type,
                'issue_description': issue_description,
                'confidence': frame_data['analysis']['confidence']
            }
            
            comparison_results.append(comparison_result)
            
            if not is_correct:
                issues_found.append(comparison_result)
        
        return {
            'total_comparisons': len(comparison_results),
            'correct_steps': len([r for r in comparison_results if r['is_correct']]),
            'incorrect_steps': len([r for r in comparison_results if not r['is_correct']]),
            'accuracy_rate': len([r for r in comparison_results if r['is_correct']]) / len(comparison_results),
            'comparison_details': comparison_results,
            'issues_found': issues_found
        }

    def save_analysis_screenshots(self, comparison_results: Dict, output_dir: str = 'analysis_output') -> None:
        """保存分析截图"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n保存分析截图到: {output_dir}")
        
        # 保存问题截图
        for i, issue in enumerate(comparison_results['issues_found']):
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            
            ax.imshow(issue['frame'])
            ax.set_title(f"问题截图 {i+1}: {issue['issue_type']}\n{issue['issue_description']}", 
                        fontsize=14, pad=20)
            ax.axis('off')
            
            # 添加时间戳
            ax.text(0.02, 0.98, f"时间: {issue['timestamp']}s", 
                   transform=ax.transAxes, fontsize=12, 
                   verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/issue_{i+1:02d}_t{issue['timestamp']}s.png", 
                       dpi=150, bbox_inches='tight')
            plt.close()
        
        # 保存正确步骤的示例截图
        correct_steps = [r for r in comparison_results['comparison_details'] if r['is_correct']]
        for i, correct in enumerate(correct_steps[:3]):  # 只保存前3个正确示例
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            
            ax.imshow(correct['frame'])
            ax.set_title(f"正确示例 {i+1}: {correct['issue_description']}", 
                        fontsize=14, pad=20)
            ax.axis('off')
            
            ax.text(0.02, 0.98, f"时间: {correct['timestamp']}s", 
                   transform=ax.transAxes, fontsize=12, 
                   verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/correct_{i+1:02d}_t{correct['timestamp']}s.png", 
                       dpi=150, bbox_inches='tight')
            plt.close()

    def generate_analysis_report(self, student_analysis: Dict, comparison_results: Dict, 
                               output_file: str = 'analysis_report.json') -> None:
        """生成详细的分析报告"""
        
        report = {
            'analysis_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'student_video': student_analysis['video_path'],
            'total_frames_analyzed': student_analysis['total_frames_analyzed'],
            'steps_completion': {
                'expected_steps': len(self.teacher_steps),
                'detected_steps': len(student_analysis['steps_detected']),
                'completion_rate': len(student_analysis['steps_detected']) / len(self.teacher_steps)
            },
            'accuracy_assessment': {
                'total_comparisons': comparison_results['total_comparisons'],
                'correct_steps': comparison_results['correct_steps'],
                'incorrect_steps': comparison_results['incorrect_steps'],
                'accuracy_rate': comparison_results['accuracy_rate']
            },
            'issues_summary': [
                {
                    'timestamp': issue['timestamp'],
                    'issue_type': issue['issue_type'],
                    'description': issue['issue_description'],
                    'expected_step': issue['expected_step']['name'] if issue['expected_step'] else 'None',
                    'detected_step': issue['student_step']['name'],
                    'confidence': issue['confidence']
                }
                for issue in comparison_results['issues_found']
            ],
            'recommendations': self.generate_recommendations(comparison_results)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {output_file}")
        return report

    def generate_recommendations(self, comparison_results: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        accuracy = comparison_results['accuracy_rate']
        issues = comparison_results['issues_found']
        
        if accuracy >= 0.8:
            recommendations.append("总体表现良好，实验步骤基本正确")
        elif accuracy >= 0.6:
            recommendations.append("实验步骤大部分正确，但仍有改进空间")
        else:
            recommendations.append("实验步骤存在较多问题，建议重新学习标准流程")
        
        # 基于问题类型生成具体建议
        issue_types = [issue['issue_type'] for issue in issues]
        
        if "步骤错误" in issue_types:
            recommendations.append("注意按照正确的顺序执行实验步骤")
        
        if "时间偏差" in issue_types:
            recommendations.append("建议控制好每个步骤的时间，避免过快或过慢")
        
        recommendations.extend([
            "建议观看教师示范视频，注意关键操作细节",
            "重点关注设备的正确使用方法",
            "实验过程中要仔细观察干涉条纹的变化"
        ])
        
        return recommendations

    def print_analysis_summary(self, report: Dict) -> None:
        """打印分析总结"""
        print("\n" + "="*60)
        print("迈克尔逊干涉实验AI分析报告")
        print("="*60)
        
        print(f"分析时间: {report['analysis_time']}")
        print(f"学生视频: {report['student_video']}")
        print(f"分析帧数: {report['total_frames_analyzed']}")
        
        print(f"\n实验完成度:")
        print(f"  预期步骤数: {report['steps_completion']['expected_steps']}")
        print(f"  检测步骤数: {report['steps_completion']['detected_steps']}")
        print(f"  完成率: {report['steps_completion']['completion_rate']:.1%}")
        
        print(f"\n准确性评估:")
        print(f"  总对比次数: {report['accuracy_assessment']['total_comparisons']}")
        print(f"  正确步骤: {report['accuracy_assessment']['correct_steps']}")
        print(f"  错误步骤: {report['accuracy_assessment']['incorrect_steps']}")
        print(f"  准确率: {report['accuracy_assessment']['accuracy_rate']:.1%}")
        
        if report['issues_summary']:
            print(f"\n发现的问题:")
            for i, issue in enumerate(report['issues_summary'], 1):
                print(f"  {i}. [t={issue['timestamp']}s] {issue['issue_type']}: {issue['description']}")
        
        print(f"\n改进建议:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")

def main():
    """主函数：运行完整的分析流程"""
    print("迈克尔逊干涉实验AI分析系统")
    print("="*60)
    
    # 初始化分析器
    analyzer = MichelsonInterferometerAnalyzer()
    
    # 设置视频路径（用户需要根据实际情况修改）
    teacher_video_path = "teacher.mp4"  # 教师示范视频
    student_video_path = "student.mp4"  # 学生实验视频
    
    try:
        # 分析学生视频
        print("步骤 1: 分析学生实验视频")
        student_analysis = analyzer.analyze_video(student_video_path, 'student')
        
        # 如果有教师视频，也可以分析（可选）
        teacher_analysis = None
        if os.path.exists(teacher_video_path):
            print("步骤 2: 分析教师示范视频（可选）")
            teacher_analysis = analyzer.analyze_video(teacher_video_path, 'teacher')
        
        # 对比分析
        print("步骤 3: 对比分析")
        comparison_results = analyzer.compare_student_with_teacher(student_analysis, teacher_analysis)
        
        # 保存截图
        print("步骤 4: 保存分析截图")
        analyzer.save_analysis_screenshots(comparison_results)
        
        # 生成报告
        print("步骤 5: 生成分析报告")
        report = analyzer.generate_analysis_report(student_analysis, comparison_results)
        
        # 打印总结
        analyzer.print_analysis_summary(report)
        
        print(f"\n分析完成！")
        print(f"- 截图保存在: analysis_output/ 目录")
        print(f"- 详细报告: analysis_report.json") 
        
    except FileNotFoundError as e:
        print(f"错误: 找不到视频文件")
        print(f"请确保以下文件存在:")
        print(f"  - {student_video_path}")
        print(f"  - {teacher_video_path} (可选)")
        print(f"\n你可以修改main()函数中的视频路径")
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
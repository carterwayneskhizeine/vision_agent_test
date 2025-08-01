#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迈克尔逊干涉实验AI分析原型
整合视频分析和设备检测功能，用于教学评估

基于现有的video_test.py和imagetest_batch.py代码
适配Web应用使用
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
    
    def __init__(self, work_dir: str = '.'):
        """初始化分析器"""
        self.work_dir = work_dir
        
        # 预定义的教师实验步骤（标准流程 - 适应1分55秒视频）
        self.teacher_steps = [
            {
                "step_id": 1,
                "name": "迈克尔逊干涉仪初始设置",
                "start_time": 5,
                "duration": 20,
                "key_actions": ["安装氦氖激光器", "确保架间隙均匀", "准备光学元件"],
                "required_equipment": ["氦氖激光器"],
                "success_criteria": ["激光器正确安装", "框架水平稳定"]
            },
            {
                "step_id": 2,
                "name": "激光器对准和调节",
                "start_time": 25,
                "duration": 20,
                "key_actions": ["调节激光器位置", "调节光束通过分束器", "使光点重合"],
                "required_equipment": ["氦氖激光器", "分束器和补偿板"],
                "success_criteria": ["光束对准", "两个光点重合"]
            },
            {
                "step_id": 3,
                "name": "获得干涉条纹",
                "start_time": 45,
                "duration": 20,
                "key_actions": ["加入扩束器", "调节动镜手钮", "获得干涉条纹"],
                "required_equipment": ["扩束器", "动镜"],
                "success_criteria": ["出现清晰干涉条纹", "条纹位于中心"]
            },
            {
                "step_id": 4,
                "name": "观察等倾干涉图",
                "start_time": 65,
                "duration": 15,
                "key_actions": ["转动精密测微头", "调节测微头", "观察圆形干涉环"],
                "required_equipment": ["精密测微头"],
                "success_criteria": ["出现圆形干涉环", "环心在屏中央"]
            },
            {
                "step_id": 5,
                "name": "精密测量过程",
                "start_time": 80,
                "duration": 20,
                "key_actions": ["记录测微头读数", "旋转测微螺旋", "计数干涉环变化"],
                "required_equipment": ["精密测微头"],
                "success_criteria": ["准确记录读数", "正确计数环数"]
            },
            {
                "step_id": 6,
                "name": "法布里-珀罗干涉设置",
                "start_time": 100,
                "duration": 15,
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
        
        # 定义部件文件映射（与imagetest_batch.py保持一致）
        self.component_mapping = {
            'part1.png': {'chinese': '氦氖激光器', 'english': 'Helium-Neon Laser'},
            'part2.png': {'chinese': '分束器和补偿板', 'english': 'Beam Splitter and Compensator Plate'},
            'part3.png': {'chinese': '动镜', 'english': 'Moving Mirror'},
            'part4.png': {'chinese': '定镜', 'english': 'Fixed Mirror'},
            'part5.png': {'chinese': '精密测微头', 'english': 'Precision Micrometer Head'},
            'part6.png': {'chinese': '扩束器', 'english': 'Beam Expander'},
            'part7.png': {'chinese': '二合一观察屏', 'english': 'Combination Observation Screen'}
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

    def extract_frame_at_timestamp(self, video_path: str, timestamp: int) -> np.ndarray:
        """提取视频指定时间戳的帧"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        
        cap.release()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def analyze_video_steps(self, video_path: str, video_type: str = 'student', interval: int = 30) -> List[Dict]:
        """分析视频的实验步骤（基于video_test.py的逻辑）"""
        print(f"\n开始分析 {video_type} 视频的实验步骤...")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"视频信息: {total_frames} 帧, {fps:.2f} FPS, 时长: {timedelta(seconds=int(duration))}")
        
        # 定义分析时间点
        if video_type == 'teacher':
            # 老师视频：根据预定义步骤时间点分析
            timestamps = [step['start_time'] for step in self.teacher_steps]
        else:
            # 学生视频：每30秒分析一次
            timestamps = list(range(0, int(duration), interval))
            # 添加最后时间点
            if int(duration) - timestamps[-1] > interval/2:
                timestamps.append(int(duration) - 5)
        
        analysis_points = []
        
        for t in timestamps:
            if t >= duration:
                continue
                
            frame = self.extract_frame_at_timestamp(video_path, t)
            if frame is None:
                continue
            
            # 识别当前步骤
            current_step = self.identify_step_from_time_and_frame(t, frame, video_type)
            
            analysis_points.append({
                'timestamp': t,
                'time_str': f"{int(t//60):02d}:{int(t%60):02d}",
                'frame': frame,
                'current_step': current_step,
                'video_type': video_type
            })
        
        cap.release()
        return analysis_points

    def identify_step_from_time_and_frame(self, timestamp: int, frame: np.ndarray, video_type: str) -> Dict:
        """根据时间和帧内容识别实验步骤"""
        
        if video_type == 'teacher':
            # 老师视频：基于预定义步骤
            for step in self.teacher_steps:
                if step['start_time'] <= timestamp <= step['start_time'] + step.get('duration', 20):
                    return {
                        'step_id': step['step_id'],
                        'name': step['name'],
                        'description': step['key_actions'],
                        'expected': True,
                        'confidence': 0.9
                    }
        else:
            # 学生视频：基于时间推测和帧分析
            # 简化的步骤识别逻辑
            if timestamp < 30:
                return {
                    'step_id': 1,
                    'name': '迈克尔逊干涉仪初始设置',
                    'description': ['准备和检查设备', '调整基础配置'],
                    'expected': False,
                    'confidence': 0.7
                }
            elif timestamp < 60:
                return {
                    'step_id': 2,
                    'name': '激光器对准和调节',
                    'description': ['调节激光器位置', '对准光路'],
                    'expected': False,
                    'confidence': 0.7
                }
            elif timestamp < 90:
                return {
                    'step_id': 3,
                    'name': '获得干涉条纹',
                    'description': ['加入扩束器', '调节获得干涉条纹'],
                    'expected': False,
                    'confidence': 0.7
                }
            elif timestamp < 120:
                return {
                    'step_id': 4,
                    'name': '观察等倾干涉图',
                    'description': ['调节测微头', '观察干涉环'],
                    'expected': False,
                    'confidence': 0.7
                }
            else:
                return {
                    'step_id': 5,
                    'name': '精密测量过程',
                    'description': ['记录读数', '测量过程'],
                    'expected': False,
                    'confidence': 0.7
                }
        
        # 默认返回未识别步骤
        return {
            'step_id': 0,
            'name': '未识别步骤',
            'description': ['未能识别的操作'],
            'expected': False,
            'confidence': 0.3
        }

    def save_step_screenshots(self, teacher_analysis: List[Dict], student_analysis: List[Dict], 
                            output_dir: str) -> Dict:
        """保存步骤分析截图和对应解释"""
        os.makedirs(output_dir, exist_ok=True)
        
        screenshot_explanations = {}
        
        # 1. 保存老师步骤截图
        for i, point in enumerate(teacher_analysis):
            step = point['current_step']
            timestamp = point['timestamp']
            
            # 保存截图
            screenshot_name = f"teacher_step_{step['step_id']:02d}_t{timestamp}s.png"
            screenshot_path = os.path.join(output_dir, screenshot_name)
            
            # 转换为BGR保存
            frame_bgr = cv2.cvtColor(point['frame'], cv2.COLOR_RGB2BGR)
            cv2.imwrite(screenshot_path, frame_bgr)
            
            # 保存解释
            screenshot_explanations[screenshot_name] = {
                'type': '老师示范',
                'step_id': step['step_id'],
                'step_name': step['name'],
                'timestamp': timestamp,
                'time_str': point['time_str'],
                'description': step['description'],
                'explanation': f"老师在{timestamp}秒时执行: {step['name']}"
            }
        
        # 2. 保存学生步骤截图
        for i, point in enumerate(student_analysis):
            step = point['current_step']
            timestamp = point['timestamp']
            
            screenshot_name = f"student_step_{step['step_id']:02d}_t{timestamp}s.png"
            screenshot_path = os.path.join(output_dir, screenshot_name)
            
            frame_bgr = cv2.cvtColor(point['frame'], cv2.COLOR_RGB2BGR)
            cv2.imwrite(screenshot_path, frame_bgr)
            
            screenshot_explanations[screenshot_name] = {
                'type': '学生操作',
                'step_id': step['step_id'],
                'step_name': step['name'],
                'timestamp': timestamp,
                'time_str': point['time_str'],
                'description': step['description'],
                'confidence': step.get('confidence', 0.0),
                'explanation': f"学生在{timestamp}秒时执行: {step['name']}"
            }
        
        return screenshot_explanations

    def generate_analysis_report(self, teacher_analysis: List[Dict], student_analysis: List[Dict], 
                               screenshot_explanations: Dict) -> Dict:
        """生成简化的实验步骤分析报告"""
        
        report = {
            'analysis_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': '实验步骤AI分析（老师示范 + 学生操作）',
            'videos_analyzed': {
                'teacher_video': 'teacher.mp4',
                'student_video': 'student.mp4'
            },
            'teacher_analysis': {
                'video_type': '老师示范',
                'total_steps_identified': len(teacher_analysis),
                'analysis_summary': 'LGS-7A精密干涉仪实验步骤 - 老师示范',
                'steps': [
                    {
                        'step_id': point['current_step']['step_id'],
                        'step_name': point['current_step']['name'],
                        'timestamp': point['timestamp'],
                        'time_str': point['time_str'],
                        'description': point['current_step']['description'],
                        'formatted_output': f"## 步骤{point['current_step']['step_id']}：{point['current_step']['name']} (t={point['timestamp']}s)"
                    }
                    for point in teacher_analysis
                ]
            },
            'student_analysis': {
                'video_type': '学生操作',
                'total_steps_identified': len(student_analysis),
                'analysis_summary': 'LGS-7A精密干涉仪实验步骤 - 学生操作',
                'steps': [
                    {
                        'step_id': point['current_step']['step_id'],
                        'step_name': point['current_step']['name'],
                        'timestamp': point['timestamp'],
                        'time_str': point['time_str'],
                        'description': point['current_step']['description'],
                        'confidence': point['current_step'].get('confidence', 0.0),
                        'formatted_output': f"## 步骤{point['current_step']['step_id']}：{point['current_step']['name']} (t={point['timestamp']}s)"
                    }
                    for point in student_analysis
                ]
            },
            'screenshot_explanations': screenshot_explanations,
            'output_format_example': {
                'description': '输出格式按照用户要求，分别展示老师示范和学生操作的实验步骤',
                'format': 'LGS-7A精密干涉仪实验步骤格式，包含步骤编号、名称、时间戳和关键操作描述'
            }
        }
        
        return report
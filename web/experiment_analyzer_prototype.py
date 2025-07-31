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

    def draw_chinese_text(self, img, text, position, font_size=24, text_color=(0, 0, 255)):
        """Draw Chinese text on image without encoding issues"""
        # 判断输入图像格式并转换为RGB用于PIL
        if len(img.shape) == 3:
            # 如果是3通道，假设是RGB格式（来自我们的处理流程）
            img_pil = Image.fromarray(img)
        else:
            # 如果是单通道，转换为RGB
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))

        # Create a drawing context
        draw = ImageDraw.Draw(img_pil)

        # 尝试多种字体路径
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # Windows SimHei
            "C:/Windows/Fonts/msyh.ttf",    # Windows Microsoft YaHei
            "C:/Windows/Fonts/simsun.ttc",  # Windows SimSun
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux
        ]
        
        font = None
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            except:
                continue
        
        if font is None:
            # Fallback to default font
            try:
                font = ImageFont.load_default()
            except:
                # 如果连默认字体都加载失败，使用OpenCV绘制
                cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
                return img

        # Draw the text
        draw.text(position, text, font=font, fill=text_color)

        # 返回RGB格式（保持与输入一致）
        return np.array(img_pil)

    def extract_template_improved(self, labeled_img):
        """Improved template extraction with better red box detection"""
        print("    改进的模板提取方法...")
        
        # Convert to different color spaces for better red detection
        hsv = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2HSV)
        
        # Multiple red detection strategies
        # Strategy 1: HSV based
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsv_mask = cv2.bitwise_or(mask1, mask2)
        
        # Strategy 2: BGR based (direct red channel)
        b, g, r = cv2.split(labeled_img)
        # Red is dominant and green/blue are low
        red_dominant = (r > 150).astype(np.uint8)
        green_low = (g < 100).astype(np.uint8)
        blue_low = (b < 100).astype(np.uint8)
        bgr_mask = cv2.bitwise_and(red_dominant, cv2.bitwise_and(green_low, blue_low)) * 255
        
        # Combine masks
        combined_mask = cv2.bitwise_or(hsv_mask, bgr_mask)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3,3), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the best rectangular contour
        best_box = None
        max_score = 0
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Filter by size and aspect ratio
            if area > 500 and w > 50 and h > 20:
                # Calculate rectangularity (how close to a rectangle)
                contour_area = cv2.contourArea(contour)
                rectangularity = contour_area / area if area > 0 else 0
                
                # Score based on area and rectangularity
                score = area * rectangularity
                
                if score > max_score:
                    max_score = score
                    best_box = (x, y, x+w, y+h)
        
        if best_box is None:
            # Fallback to manual detection
            h, w = labeled_img.shape[:2]
            best_box = (int(0.11*w), int(0.16*h), int(0.30*w), int(0.22*h))
            print("      使用手动估计的边界框")
        else:
            print(f"      自动检测到红色边界框: {best_box}")
        
        x1, y1, x2, y2 = best_box
        template = labeled_img[y1:y2, x1:x2]
        
        return template, best_box

    def multi_scale_template_matching(self, target_img, template, scales=[0.8, 0.9, 1.0, 1.1, 1.2]):
        """Multi-scale template matching for better accuracy"""
        print("    执行多尺度模板匹配...")
        
        best_match = None
        best_score = 0
        best_scale = 1.0
        
        template_h, template_w = template.shape[:2]
        
        for scale in scales:
            # Resize template
            new_w = int(template_w * scale)
            new_h = int(template_h * scale)
            
            if new_w <= 0 or new_h <= 0 or new_w > target_img.shape[1] or new_h > target_img.shape[0]:
                continue
                
            scaled_template = cv2.resize(template, (new_w, new_h))
            
            # Template matching with multiple methods
            methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF_NORMED]
            
            for method in methods:
                result = cv2.matchTemplate(target_img, scaled_template, method)
                
                if method == cv2.TM_SQDIFF_NORMED:
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    score = 1 - min_val  # Convert to similarity score
                    loc = min_loc
                else:
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    score = max_val
                    loc = max_loc
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        'location': loc,
                        'size': (new_w, new_h),
                        'score': score,
                        'scale': scale,
                        'method': method
                    }
        
        return best_match

    def feature_based_matching(self, target_img, template):
        """Feature-based matching using SIFT/ORB as backup"""
        print("    尝试基于特征点的匹配...")
        
        try:
            # Try SIFT first
            try:
                sift = cv2.SIFT_create()
                kp1, des1 = sift.detectAndCompute(template, None)
                kp2, des2 = sift.detectAndCompute(target_img, None)
                detector_name = "SIFT"
            except:
                # Fallback to ORB
                orb = cv2.ORB_create()
                kp1, des1 = orb.detectAndCompute(template, None)
                kp2, des2 = orb.detectAndCompute(target_img, None)
                detector_name = "ORB"
            
            if des1 is None or des2 is None:
                return None
                
            print(f"      使用{detector_name}检测到模板特征点: {len(kp1)}, 目标图像特征点: {len(kp2)}")
            
            # Match features
            if detector_name == "SIFT":
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1, des2, k=2)
                
                # Apply ratio test
                good_matches = []
                for match_pair in matches:
                    if len(match_pair) == 2:
                        m, n = match_pair
                        if m.distance < 0.75 * n.distance:
                            good_matches.append(m)
            else:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)
                good_matches = sorted(matches, key=lambda x: x.distance)[:50]
            
            print(f"      找到{len(good_matches)}个有效匹配点")
            
            if len(good_matches) >= 4:
                # Extract matched keypoints
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                # Find homography
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
                if M is not None:
                    # Transform template corners to target image
                    h, w = template.shape[:2]
                    corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
                    transformed_corners = cv2.perspectiveTransform(corners, M)
                    
                    # Calculate bounding box
                    x_coords = transformed_corners[:, 0, 0]
                    y_coords = transformed_corners[:, 0, 1]
                    
                    x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
                    y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))
                    
                    # Calculate match quality based on inliers
                    inliers = np.sum(mask)
                    quality = inliers / len(good_matches)
                    
                    return {
                        'location': (x_min, y_min),
                        'size': (x_max - x_min, y_max - y_min),
                        'score': quality,
                        'method': f'{detector_name}_HOMOGRAPHY'
                    }
            
            return None
            
        except Exception as e:
            print(f"      特征匹配失败: {e}")
            return None

    def detect_single_component(self, labeled_img_path, target_img, component_name, min_confidence=0.3):
        """Detect a single component in the target image"""
        
        # Load labeled image
        if not os.path.exists(labeled_img_path):
            print(f"    错误: 标注文件 {labeled_img_path} 不存在")
            return None
            
        labeled_img = cv2.imread(labeled_img_path)
        if labeled_img is None:
            print(f"    错误: 无法加载标注图片 {labeled_img_path}")
            return None

        print(f"    标注图片尺寸: {labeled_img.shape}")

        # Extract template with improved method
        template, template_box = self.extract_template_improved(labeled_img)
        x1, y1, x2, y2 = template_box
        print(f"    提取的模板区域: ({x1}, {y1}) - ({x2}, {y2})")
        print(f"    模板尺寸: {template.shape}")

        # Method 1: Multi-scale template matching
        multi_scale_result = self.multi_scale_template_matching(target_img, template)
        
        # Method 2: Feature-based matching
        feature_result = self.feature_based_matching(target_img, template)
        
        # Choose the best result
        best_result = None
        method_used = "无"
        
        if multi_scale_result and feature_result:
            if multi_scale_result['score'] > feature_result['score']:
                best_result = multi_scale_result
                method_used = f"多尺度模板匹配 (尺度: {multi_scale_result['scale']:.1f})"
            else:
                best_result = feature_result
                method_used = "特征点匹配"
        elif multi_scale_result:
            best_result = multi_scale_result
            method_used = f"多尺度模板匹配 (尺度: {multi_scale_result['scale']:.1f})"
        elif feature_result:
            best_result = feature_result
            method_used = "特征点匹配"
        else:
            # Fallback to basic template matching
            print("    所有高级方法失败，使用基础模板匹配")
            result = cv2.matchTemplate(target_img, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            best_result = {
                'location': max_loc,
                'size': (template.shape[1], template.shape[0]),
                'score': max_val
            }
            method_used = "基础模板匹配"

        # Check if confidence is above threshold
        if best_result['score'] < min_confidence:
            print(f"    检测置信度 {best_result['score']:.3f} 低于阈值 {min_confidence}，认为未检测到")
            return None

        # Extract detection information
        top_left = best_result['location']
        w, h = best_result['size']
        bottom_right = (top_left[0] + w, top_left[1] + h)
        score = best_result['score']

        print(f"    最佳检测方法: {method_used}")
        print(f"    检测置信度: {score:.3f}")
        print(f"    检测到的组件位置: {top_left} - {bottom_right}")
        print(f"    组件大小: {w} x {h} 像素")

        return {
            'name': component_name,
            'bbox': (top_left[0], top_left[1], bottom_right[0], bottom_right[1]),
            'confidence': score,
            'score': score,  # 兼容imagetest_batch.py格式
            'method': method_used,
            'component_name': component_name  # 兼容imagetest_batch.py格式
        }

    def detect_equipment_in_frame(self, frame: np.ndarray, min_confidence: float = 0.3) -> List[Dict]:
        """在帧中检测实验设备（真实检测版本）"""
        print("  正在进行实验设备检测...")
        
        detections = []
        
        # 确保frame是BGR格式用于OpenCV处理（与imagetest_batch.py保持一致）
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            # 如果是RGB格式，转换为BGR用于OpenCV
            target_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        else:
            target_img = frame.copy()
        
        print(f"目标图片尺寸: {target_img.shape}")
        print("="*70)
        
        # 遍历每个部件模板进行检测（与imagetest_batch.py保持一致的顺序和逻辑）
        detected_count = 0
        for i, (part_file, component_info) in enumerate(self.component_mapping.items()):
            print(f"\n[{i+1}/7] 正在检测: {component_info['chinese']} ({component_info['english']})")
            print(f"使用标注文件: {part_file}")
            
            # 检查标注文件是否存在
            if not os.path.exists(part_file):
                print(f"  警告: 标注文件 {part_file} 不存在，跳过")
                continue
            
            # 检测单个组件（使用与imagetest_batch.py相同的参数）
            detection = self.detect_single_component(
                part_file, 
                target_img, 
                component_info['chinese'], 
                min_confidence
            )
            
            if detection:
                detected_count += 1
                detections.append(detection)
                print(f"  ✅ 检测成功!")
            else:
                print(f"  ❌ 未检测到")
        
        # 输出汇总信息（与imagetest_batch.py保持一致）
        print("\n" + "="*70)
        print("检测结果汇总:")
        print("="*70)
        print(f"总计检测部件数: {len(self.component_mapping)}")
        print(f"成功检测部件数: {detected_count}")
        print(f"检测成功率: {detected_count/len(self.component_mapping)*100:.1f}%")
        
        return detections

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
            equipment_detections = self.detect_equipment_in_frame(frame_data['frame'], min_confidence=0.25)
            
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
                'confidence': frame_data['analysis']['confidence'],
                'detected_equipment': frame_data['analysis']['detected_equipment']
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

    def draw_detections_on_frame(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """在帧上绘制检测结果"""
        result_frame = frame.copy()
        
        for i, detection in enumerate(detections):
            name = detection['name']
            bbox = detection['bbox']
            confidence = detection['confidence']
            
            x1, y1, x2, y2 = bbox
            color = self.colors[i % len(self.colors)]
            
            # 绘制边界框
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 3)
            
            # 使用改进的中文文本绘制
            text_position = (x1, max(30, y1 - 10))
            result_frame = self.draw_chinese_text(
                result_frame,
                name,
                text_position,
                font_size=30,
                text_color=color
            )
            
            # 在右下角添加置信度信息（使用英文，避免字体问题）
            confidence_text = f"{confidence:.3f}"
            cv2.putText(result_frame, confidence_text, (x1, y2 + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
        return result_frame

    def save_analysis_screenshots(self, comparison_results: Dict, output_dir: str = 'analysis_output') -> None:
        """保存分析截图"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n保存分析截图到: {output_dir}")
        
        # 保存问题截图
        for i, issue in enumerate(comparison_results['issues_found']):
            fig, ax = plt.subplots(1, 1, figsize=(15, 10))
            
            # 获取检测结果并绘制
            detections = issue.get('detected_equipment', [])
            annotated_frame = self.draw_detections_on_frame(issue['frame'], detections)
            
            ax.imshow(annotated_frame)
            ax.set_title(f"问题截图 {i+1}: {issue['issue_type']}\n{issue['issue_description']}", 
                        fontsize=14, pad=20)
            ax.axis('off')
            
            # 添加时间戳
            ax.text(0.02, 0.98, f"时间: {issue['timestamp']}s", 
                   transform=ax.transAxes, fontsize=12, 
                   verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
            
            # 添加检测信息
            if detections:
                detection_info = f"检测到设备: {', '.join([d['name'] for d in detections])}"
                ax.text(0.02, 0.02, detection_info, 
                       transform=ax.transAxes, fontsize=10, 
                       verticalalignment='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/issue_{i+1:02d}_t{issue['timestamp']}s.png", 
                       dpi=150, bbox_inches='tight')
            plt.close()
        
        # 保存正确步骤的示例截图
        correct_steps = [r for r in comparison_results['comparison_details'] if r['is_correct']]
        for i, correct in enumerate(correct_steps[:3]):  # 只保存前3个正确示例
            fig, ax = plt.subplots(1, 1, figsize=(15, 10))
            
            # 获取检测结果并绘制
            detections = correct.get('detected_equipment', [])
            annotated_frame = self.draw_detections_on_frame(correct['frame'], detections)
            
            ax.imshow(annotated_frame)
            ax.set_title(f"正确示例 {i+1}: {correct['issue_description']}", 
                        fontsize=14, pad=20)
            ax.axis('off')
            
            ax.text(0.02, 0.98, f"时间: {correct['timestamp']}s", 
                   transform=ax.transAxes, fontsize=12, 
                   verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            
            # 添加检测信息
            if detections:
                detection_info = f"检测到设备: {', '.join([d['name'] for d in detections])}"
                ax.text(0.02, 0.02, detection_info, 
                       transform=ax.transAxes, fontsize=10, 
                       verticalalignment='bottom',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            
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

def extract_frame_at_time(video_path: str, time_seconds: float = 113.0, output_path: str = 'Identify_target.png'):
    """提取视频指定时间点的帧作为目标图片"""
    print(f"正在提取 {video_path} 在 {time_seconds}秒 的帧...")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")
    
    # 获取视频信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    
    print(f"视频信息: {total_frames} 帧, {fps:.2f} FPS, 时长: {timedelta(seconds=int(duration))}")
    
    # 检查时间点是否有效
    if time_seconds > duration:
        print(f"⚠️  指定时间 {time_seconds}秒 超过视频总时长 {duration:.1f}秒，将提取最后一帧")
        target_frame_number = total_frames - 1
        time_seconds = duration
    else:
        # 计算目标帧号
        target_frame_number = int(time_seconds * fps)
    
    print(f"目标时间: {time_seconds}秒 (第 {target_frame_number} 帧)")
    
    # 跳到指定帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_number)
    ret, frame = cap.read()
    
    if ret:
        # 保存指定时间的帧
        cv2.imwrite(output_path, frame)
        print(f"✅ {time_seconds}秒的帧已保存为: {output_path}")
        print(f"图片尺寸: {frame.shape}")
        cap.release()
        return frame
    else:
        cap.release()
        raise ValueError(f"无法读取视频在 {time_seconds}秒 的帧")

def analyze_single_frame_detection():
    """只分析单帧的设备检测功能"""
    print("迈克尔逊干涉实验设备检测系统")
    print("="*60)
    
    # 检查必需的文件
    required_files = {
        'student.mp4': '学生实验视频',
        'part1.png': '氦氖激光器标注图片',
        'part2.png': '分束器和补偿板标注图片',
        'part3.png': '动镜标注图片',
        'part4.png': '定镜标注图片',
        'part5.png': '精密测微头标注图片',
        'part6.png': '扩束器标注图片'
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if not os.path.exists(file_path):
            missing_files.append(f"  ❌ {file_path} - {description}")
        else:
            print(f"  ✅ {file_path} - {description}")
    
    if missing_files:
        print(f"\n缺少以下必需文件:")
        for missing in missing_files:
            print(missing)
        print(f"\n请确保所有文件都在 web/ 目录中，然后重新运行程序。")
        return False
    
    # 可选文件检查
    if os.path.exists('part7.png'):
        print(f"  ✅ part7.png - 二合一观察屏标注图片")
    else:
        print(f"  ⚪ part7.png - 二合一观察屏标注图片 (可选)")
    
    try:
        # 初始化分析器
        analyzer = MichelsonInterferometerAnalyzer()
        
        # 步骤1: 提取指定时间的帧作为目标图片  
        print(f"\n{'='*60}")
        print("步骤 1: 提取student.mp4在1分48秒的帧作为Identify_target.png")
        print("="*60)
        
        target_frame = extract_frame_at_time('student.mp4', time_seconds=108.0, output_path='Identify_target.png')
        
        # 步骤2: 对1分48秒的帧进行设备检测
        print(f"\n{'='*60}")
        print("步骤 2: 对1分48秒的帧进行设备检测")
        print("="*60)
        
        # 转换为RGB格式用于分析
        target_frame_rgb = cv2.cvtColor(target_frame, cv2.COLOR_BGR2RGB)
        
        # 执行设备检测
        equipment_detections = analyzer.detect_equipment_in_frame(target_frame_rgb, min_confidence=0.25)
        
        # 步骤3: 保存检测结果图片
        print(f"\n{'='*60}")
        print("步骤 3: 保存检测结果")
        print("="*60)
        
        if equipment_detections:
            # 在原图上绘制检测结果
            annotated_frame = analyzer.draw_detections_on_frame(target_frame_rgb, equipment_detections)
            
            # 保存标注后的图片
            annotated_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite('detection_result.png', annotated_bgr)
            
            print(f"✅ 检测结果已保存:")
            print(f"  📸 1分48秒的帧: Identify_target.png")
            print(f"  📸 标注检测结果: detection_result.png")
            
            # 生成检测报告
            print(f"\n{'='*60}")
            print("检测结果报告")
            print("="*60)
            
            print(f"检测到的设备数量: {len(equipment_detections)}")
            print(f"检测成功率: {len(equipment_detections)}/7 = {len(equipment_detections)/7*100:.1f}%")
            
            print(f"\n详细检测结果:")
            for i, detection in enumerate(equipment_detections, 1):
                name = detection['name']
                confidence = detection['confidence']
                bbox = detection['bbox']
                method = detection['method']
                x1, y1, x2, y2 = bbox
                
                print(f"  {i}. {name}")
                print(f"     置信度: {confidence:.3f}")
                print(f"     位置: ({x1}, {y1}) - ({x2}, {y2})")
                print(f"     大小: {x2-x1} x {y2-y1} 像素")
                print(f"     方法: {method}")
                print()
            
            # 保存JSON报告
            detection_report = {
                'analysis_time': time.strftime('%Y-%m-%d %H:%M:%S'),
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
            
            print(f"📋 详细报告: detection_report.json")
            
        else:
            print("❌ 未检测到任何设备")
        
        print(f"\n🎉 单帧设备检测完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数：运行设备检测分析"""
    print("迈克尔逊干涉实验设备检测系统")
    print("="*60)
    
    # 检查是否有必需文件
    if os.path.exists('student.mp4') and any(os.path.exists(f'part{i}.png') for i in range(1, 7)):
        print("检测到学生视频和标注文件，启动设备检测模式...")
        success = analyze_single_frame_detection()
        if success:
            print("\n🎉 设备检测完成！")
        else:
            print("\n💡 如果遇到问题，请检查文件是否完整")
    else:
        print("未检测到必需的文件，请确保以下文件存在:")
        print("  - student.mp4 (学生实验视频)")
        print("  - part1.png 到 part6.png (设备标注图片)")
        print("\n💡 程序将:")
        print("  1. 提取student.mp4在1分48秒的帧作为Identify_target.png")
        print("  2. 使用part1-6.png检测1分48秒帧中的实验设备")
        print("  3. 生成带标注的检测结果图片")
        print("  4. 输出详细的检测报告")

if __name__ == "__main__":
    main()
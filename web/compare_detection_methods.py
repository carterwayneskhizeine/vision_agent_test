#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较两种检测方法的结果
验证 experiment_analyzer_prototype.py 和 imagetest_batch.py 的检测一致性
"""

import cv2
import numpy as np
import sys
import os

# 添加路径以便导入模块
sys.path.append('../images')

# 导入两个模块的检测函数
from experiment_analyzer_prototype import MichelsonInterferometerAnalyzer, extract_frame_at_time

def compare_detection_methods(video_path='student.mp4', time_seconds=113.0):
    """比较两种检测方法的结果"""
    
    print("🔍 检测方法对比测试")
    print("="*80)
    
    # 检查必需文件
    required_files = ['student.mp4'] + [f'part{i}.png' for i in range(1, 7)]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    
    try:
        # 1. 提取测试帧
        print("📸 步骤1: 提取测试帧")
        target_frame = extract_frame_at_time(video_path, time_seconds, 'compare_target.png')
        target_frame_rgb = cv2.cvtColor(target_frame, cv2.COLOR_BGR2RGB)
        
        # 2. 使用 experiment_analyzer_prototype.py 的方法
        print(f"\n🔬 步骤2: 使用 experiment_analyzer_prototype.py 检测")
        print("-" * 80)
        
        analyzer = MichelsonInterferometerAnalyzer()
        detections1 = analyzer.detect_equipment_in_frame(target_frame_rgb, min_confidence=0.25)
        
        # 保存检测结果1
        if detections1:
            annotated_frame1 = analyzer.draw_detections_on_frame(target_frame_rgb, detections1)
            annotated_bgr1 = cv2.cvtColor(annotated_frame1, cv2.COLOR_RGB2BGR)
            cv2.imwrite('detection_result_method1.png', annotated_bgr1)
        
        # 3. 使用 imagetest_batch.py 的方法（模拟）
        print(f"\n🔬 步骤3: 使用类似 imagetest_batch.py 的检测方法")
        print("-" * 80)
        
        # 直接使用BGR格式的图像（与imagetest_batch.py一致）
        target_img_bgr = cv2.cvtColor(target_frame_rgb, cv2.COLOR_RGB2BGR)
        
        detections2 = []
        detected_count = 0
        
        component_mapping = {
            'part1.png': {'chinese': '氦氖激光器', 'english': 'Helium-Neon Laser'},
            'part2.png': {'chinese': '分束器和补偿板', 'english': 'Beam Splitter and Compensator Plate'},
            'part3.png': {'chinese': '动镜', 'english': 'Moving Mirror'},
            'part4.png': {'chinese': '定镜', 'english': 'Fixed Mirror'},
            'part5.png': {'chinese': '精密测微头', 'english': 'Precision Micrometer Head'},
            'part6.png': {'chinese': '扩束器', 'english': 'Beam Expander'},
            'part7.png': {'chinese': '二合一观察屏', 'english': 'Combination Observation Screen'}
        }
        
        print(f"目标图片尺寸: {target_img_bgr.shape}")
        print("="*70)
        
        for i, (part_file, component_info) in enumerate(component_mapping.items()):
            if not os.path.exists(part_file):
                continue
                
            print(f"\n[{i+1}/7] 正在检测: {component_info['chinese']} ({component_info['english']})")
            print(f"使用标注文件: {part_file}")
            
            # 使用analyzer的detect_single_component方法，但使用BGR图像
            detection = analyzer.detect_single_component(
                part_file, 
                target_img_bgr, 
                component_info['chinese'], 
                0.25
            )
            
            if detection:
                detected_count += 1
                detections2.append(detection)
                print(f"  ✅ 检测成功!")
            else:
                print(f"  ❌ 未检测到")
        
        print("\n" + "="*70)
        print("检测结果汇总:")
        print("="*70)
        print(f"总计检测部件数: {len(component_mapping)}")
        print(f"成功检测部件数: {detected_count}")
        print(f"检测成功率: {detected_count/len(component_mapping)*100:.1f}%")
        
        # 4. 比较结果
        print(f"\n📊 步骤4: 结果对比")
        print("="*80)
        
        print(f"方法1 (experiment_analyzer_prototype.py): 检测到 {len(detections1)} 个设备")
        print(f"方法2 (imagetest_batch.py风格):        检测到 {len(detections2)} 个设备")
        
        if len(detections1) == len(detections2):
            print("✅ 检测数量一致")
        else:
            print("❌ 检测数量不一致")
        
        # 详细对比
        print(f"\n详细对比:")
        print("-" * 80)
        
        # 按名称对比
        det1_dict = {d['name']: d for d in detections1}
        det2_dict = {d['name']: d for d in detections2}
        
        all_names = set(det1_dict.keys()) | set(det2_dict.keys())
        
        for name in sorted(all_names):
            det1 = det1_dict.get(name)
            det2 = det2_dict.get(name)
            
            print(f"\n🔧 {name}:")
            
            if det1 and det2:
                print(f"  方法1: 置信度={det1['confidence']:.3f}, 位置={det1['bbox']}")
                print(f"  方法2: 置信度={det2['confidence']:.3f}, 位置={det2['bbox']}")
                
                # 计算置信度差异
                conf_diff = abs(det1['confidence'] - det2['confidence'])
                if conf_diff < 0.01:
                    print(f"  ✅ 置信度基本一致 (差异: {conf_diff:.4f})")
                else:
                    print(f"  ⚠️  置信度有差异 (差异: {conf_diff:.4f})")
                    
            elif det1:
                print(f"  ❌ 仅方法1检测到: 置信度={det1['confidence']:.3f}")
            elif det2:
                print(f"  ❌ 仅方法2检测到: 置信度={det2['confidence']:.3f}")
        
        # 5. 总结
        print(f"\n📋 总结:")
        print("="*80)
        
        if len(detections1) == len(detections2):
            common_count = len(set(det1_dict.keys()) & set(det2_dict.keys()))
            print(f"✅ 两种方法都检测到 {len(detections1)} 个设备")
            print(f"✅ 共同检测到的设备: {common_count} 个")
            
            if common_count == len(detections1):
                print("🎉 两种方法的检测结果完全一致！")
                return True
            else:
                print("⚠️  检测到的设备有部分差异")
                return False
        else:
            print("❌ 两种方法的检测数量不一致")
            return False
            
    except Exception as e:
        print(f"❌ 对比测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔍 迈克尔逊干涉实验设备检测方法对比工具")
    print("用于验证两种检测方法的一致性")
    print("="*80)
    
    success = compare_detection_methods()
    
    if success:
        print("\n🎉 对比测试完成，两种方法结果一致！")
        print("📁 生成的对比文件:")
        print("  📸 compare_target.png - 测试用的目标帧")
        print("  📸 detection_result_method1.png - 方法1的检测结果")
    else:
        print("\n⚠️  对比测试发现差异，需要进一步调试")

if __name__ == "__main__":
    main()
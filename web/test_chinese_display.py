#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文显示修复效果
"""

import cv2
import numpy as np
import os
from experiment_analyzer_prototype import MichelsonInterferometerAnalyzer, extract_frame_at_time

def test_chinese_display(video_path='student.mp4', time_seconds=113.0):
    """测试中文显示效果"""
    
    print("🔤 中文显示测试")
    print("="*60)
    
    # 检查必需文件
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return False
    
    part_files = [f'part{i}.png' for i in range(1, 7)]
    missing_parts = [f for f in part_files if not os.path.exists(f)]
    
    if missing_parts:
        print(f"❌ 缺少标注文件: {missing_parts}")
        return False
    
    try:
        # 1. 提取测试帧
        print("📸 提取测试帧...")
        target_frame = extract_frame_at_time(video_path, time_seconds, 'test_chinese_target.png')
        target_frame_rgb = cv2.cvtColor(target_frame, cv2.COLOR_BGR2RGB)
        
        # 2. 执行检测
        print("\n🔍 执行设备检测...")
        analyzer = MichelsonInterferometerAnalyzer()
        detections = analyzer.detect_equipment_in_frame(target_frame_rgb, min_confidence=0.25)
        
        if not detections:
            print("❌ 未检测到任何设备")
            return False
        
        # 3. 测试中文显示
        print(f"\n🎨 测试中文显示 (检测到 {len(detections)} 个设备)...")
        
        # 绘制检测结果
        annotated_frame = analyzer.draw_detections_on_frame(target_frame_rgb, detections)
        
        # 保存结果
        annotated_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite('test_chinese_result.png', annotated_bgr)
        
        print("✅ 中文显示测试完成！")
        print("\n📁 生成的文件:")
        print("  📸 test_chinese_target.png - 原始测试帧")
        print("  📸 test_chinese_result.png - 带中文标注的检测结果")
        
        print(f"\n📊 检测结果:")
        for i, detection in enumerate(detections, 1):
            name = detection['name']
            confidence = detection['confidence']
            bbox = detection['bbox']
            method = detection['method']
            
            print(f"  {i}. {name}")
            print(f"     置信度: {confidence:.3f}")
            print(f"     位置: {bbox}")
            print(f"     方法: {method}")
        
        print(f"\n💡 请查看 test_chinese_result.png 确认中文显示是否正常")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔤 迈克尔逊干涉实验中文显示测试工具")
    print("用于验证中文字体显示修复效果")
    print("="*60)
    
    success = test_chinese_display()
    
    if success:
        print("\n🎉 中文显示测试完成！")
        print("💡 请检查生成的图片文件确认显示效果")
    else:
        print("\n❌ 中文显示测试失败")

if __name__ == "__main__":
    main()
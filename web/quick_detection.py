#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速设备检测脚本

功能：
1. 提取student.mp4在1分48秒的帧作为Identify_target.png
2. 使用part1-6.png对1分48秒帧进行设备检测
3. 生成带标注的检测结果图片和详细报告

使用方法：
python quick_detection.py
"""

from experiment_analyzer_prototype import analyze_single_frame_detection

if __name__ == "__main__":
    print("🚀 快速设备检测模式") 
    print("只检测student.mp4在1分48秒的帧，不进行复杂的视频分析")
    print("-" * 50)
    
    success = analyze_single_frame_detection()
    
    if success:
        print("\n✅ 快速检测成功完成！")
        print("\n📁 生成的文件:")
        print("  📸 Identify_target.png - 学生视频1分48秒的帧")
        print("  📸 detection_result.png - 带设备标注的检测结果")
        print("  📋 detection_report.json - 详细检测报告")
        print("\n💡 可以查看detection_result.png验证设备检测效果")
    else:
        print("\n❌ 检测失败，请检查错误信息")
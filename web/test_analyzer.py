#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试迈克尔逊干涉实验AI分析原型

使用示例视频来测试分析功能
"""

import os
import sys
import cv2
import numpy as np
from experiment_analyzer_prototype import MichelsonInterferometerAnalyzer

def create_sample_video(filename: str, duration: int = 120, fps: int = 30):
    """创建一个示例视频用于测试"""
    print(f"创建示例视频: {filename}")
    
    # 视频参数
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    for frame_num in range(total_frames):
        # 创建一个简单的测试帧
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50  # 深灰色背景
        
        # 添加时间戳
        timestamp = frame_num / fps
        cv2.putText(frame, f"Time: {timestamp:.1f}s", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 根据时间添加不同的"实验步骤"内容
        if timestamp < 25:
            # 模拟初始设置阶段
            cv2.rectangle(frame, (50, 100), (150, 200), (0, 255, 0), 2)  # 绿色矩形代表激光器
            cv2.putText(frame, "Setup Phase", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        elif timestamp < 45:
            # 模拟对准阶段
            cv2.rectangle(frame, (50, 100), (150, 200), (0, 255, 0), 2)  # 激光器
            cv2.rectangle(frame, (300, 150), (400, 250), (255, 0, 0), 2)  # 蓝色矩形代表分束器
            cv2.putText(frame, "Alignment Phase", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        elif timestamp < 60:
            # 模拟获得干涉条纹
            cv2.rectangle(frame, (50, 100), (150, 200), (0, 255, 0), 2)  # 激光器
            cv2.rectangle(frame, (300, 150), (400, 250), (255, 0, 0), 2)  # 分束器
            cv2.rectangle(frame, (500, 100), (580, 180), (0, 255, 255), 2)  # 黄色矩形代表扩束器
            # 绘制简单的干涉条纹
            for i in range(5):
                y = 300 + i * 20
                cv2.line(frame, (200, y), (450, y), (255, 255, 255), 2)
            cv2.putText(frame, "Interference Pattern", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        elif timestamp < 75:
            # 模拟观察干涉图
            cv2.rectangle(frame, (50, 100), (150, 200), (0, 255, 0), 2)
            cv2.rectangle(frame, (300, 150), (400, 250), (255, 0, 0), 2)
            cv2.rectangle(frame, (500, 100), (580, 180), (0, 255, 255), 2)
            # 绘制圆形干涉环
            cv2.circle(frame, (325, 350), 50, (255, 255, 255), 2)
            cv2.circle(frame, (325, 350), 30, (255, 255, 255), 2)
            cv2.circle(frame, (325, 350), 10, (255, 255, 255), 2)
            cv2.putText(frame, "Ring Pattern", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            # 模拟测量阶段
            cv2.rectangle(frame, (50, 100), (150, 200), (0, 255, 0), 2)
            cv2.rectangle(frame, (300, 150), (400, 250), (255, 0, 0), 2)
            cv2.rectangle(frame, (450, 200), (550, 300), (128, 0, 128), 2)  # 紫色矩形代表测微头
            cv2.putText(frame, "Measurement Phase", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 128), 2)
        
        out.write(frame)
        
        # 显示进度
        if frame_num % (fps * 10) == 0:  # 每10秒显示一次进度
            progress = (frame_num / total_frames) * 100
            print(f"  进度: {progress:.1f}%")
    
    out.release()
    print(f"示例视频创建完成: {filename}")

def test_analyzer_with_sample_videos():
    """使用示例视频测试分析器"""
    print("迈克尔逊干涉实验AI分析原型测试")
    print("="*50)
    
    # 创建示例视频（如果不存在）
    teacher_video = "teacher_sample.mp4"
    student_video = "student_sample.mp4"
    
    # 创建教师示范视频（标准流程）
    if not os.path.exists(teacher_video):
        create_sample_video(teacher_video, duration=120, fps=30)
    
    # 创建学生实验视频（可能有些步骤不完整或错误）
    if not os.path.exists(student_video):
        create_sample_video(student_video, duration=100, fps=30)  # 比教师视频短一些，模拟未完成所有步骤
    
    # 初始化分析器
    analyzer = MichelsonInterferometerAnalyzer()
    
    try:
        # 分析学生视频
        print("\n分析学生实验视频...")
        student_analysis = analyzer.analyze_video(student_video, 'student')
        
        # 对比分析
        print("\n进行对比分析...")
        comparison_results = analyzer.compare_student_with_teacher(student_analysis)
        
        # 保存截图
        print("\n保存分析截图...")
        analyzer.save_analysis_screenshots(comparison_results, 'test_output')
        
        # 生成报告
        print("\n生成分析报告...")
        report = analyzer.generate_analysis_report(student_analysis, comparison_results, 'test_analysis_report.json')
        
        # 打印总结
        analyzer.print_analysis_summary(report)
        
        print(f"\n测试完成！")
        print(f"- 截图保存在: test_output/ 目录")
        print(f"- 详细报告: test_analysis_report.json")
        print(f"- 示例视频: {teacher_video}, {student_video}")
        
        return True
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    success = test_analyzer_with_sample_videos()
    
    if success:
        print("\n✅ 原型测试成功！")
        print("\n接下来你可以：")
        print("1. 用真实的实验视频替换示例视频")
        print("2. 改进设备检测算法（integrate imagetest_batch.py）")
        print("3. 增强步骤识别的准确性")
        print("4. 开发Web界面")
    else:
        print("\n❌ 原型测试失败，请检查错误信息")

if __name__ == "__main__":
    main()
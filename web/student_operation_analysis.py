#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验步骤AI视频分析脚本

专门用于分析实验步骤的AI视频分析功能：
1. AI分析teacher.mp4的实验步骤
2. AI分析student.mp4的实验步骤  
3. 分别输出老师示范和学生操作的步骤分析
4. 保存关键步骤截图和详细解释
5. 生成完整的AI分析报告

使用方法：
python student_operation_analysis.py
"""

from experiment_analyzer_prototype import analyze_student_operation_full
import os

def main():
    """运行实验步骤AI视频分析"""
    print("🎓 实验步骤AI视频分析系统")
    print("基于迈克尔逊干涉实验的教学视频AI分析")
    print("="*80)
    
    # 检查必需文件
    print("🔍 检查必需的视频文件...")
    
    required_files = ['teacher.mp4', 'student.mp4']
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ 缺少必需文件: {', '.join(missing_files)}")
        print("\n💡 请确保以下文件在web/目录中:")
        print("  📹 teacher.mp4 - 老师示范视频")
        print("  📹 student.mp4 - 学生实验视频")
        print("\n🎯 本程序将执行以下AI分析:")
        print("  1. 分析老师示范的标准实验步骤")
        print("  2. 分析学生实际的实验操作")
        print("  3. 分别输出老师和学生的步骤分析")
        print("  4. 自动保存关键步骤截图和解释")
        print("  5. 生成详细的AI分析报告")
        return
    
    # 执行完整分析
    print("\n🚀 开始AI视频分析...")
    success = analyze_student_operation_full()
    
    if success:
        print("\n" + "="*80)
        print("🎉 实验步骤AI视频分析完成！")
        print("="*80)
        
        print("\n📁 查看生成的分析结果:")
        print("  📂 step_analysis_output/ - 包含所有分析截图")
        print("    📸 teacher_step_XX_tXXs.png - 老师示范步骤截图")
        print("    📸 student_step_XX_tXXs.png - 学生操作步骤截图")
        print("  📋 experiment_steps_analysis.json - 完整AI分析报告")
        print("  📋 screenshot_explanations.json - 每张截图的详细解释")
        
        print("\n💡 使用建议:")
        print("  1. 查看experiment_steps_analysis.json了解整体分析结果")
        print("  2. 查看screenshot_explanations.json了解每张截图的解释")
        print("  3. 控制台已输出LGS-7A格式的步骤分析")
        
    else:
        print("\n❌ 分析过程中出现问题")
        print("💡 请检查视频文件是否完整且可播放")

if __name__ == "__main__":
    main()
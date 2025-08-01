# 快速开始指南

## 🚀 5分钟快速体验

### 1. 安装依赖
```bash
cd web
pip install -r requirements.txt
```

### 2. 运行测试
```bash
python test_analyzer.py
```

这将：
- 自动创建示例视频文件
- 运行完整的分析流程
- 生成截图和报告

### 3. 查看结果
运行完成后，查看以下文件：
- `test_output/` 文件夹中的截图
- `test_analysis_report.json` 详细报告

## 📁 使用真实视频

### 1. 准备视频文件
将你的视频文件放在 `web/` 目录下：
- `teacher.mp4` - 教师示范视频
- `student.mp4` - 学生实验视频

### 2. 运行分析
```bash
python experiment_analyzer_prototype.py
```

### 3. 自定义分析
编辑 `experiment_analyzer_prototype.py` 中的 `main()` 函数，修改视频路径：

```python
def main():
    analyzer = MichelsonInterferometerAnalyzer()
    
    # 修改这里的路径
    teacher_video_path = "你的教师视频.mp4"
    student_video_path = "你的学生视频.mp4"
    
    # ... 其余代码保持不变
```

## 🎯 核心功能预览

### 输出示例
```
迈克尔逊干涉实验AI分析报告
============================================================
分析时间: 2025-08-01 14:30:25
学生视频: student.mp4
分析帧数: 8

实验完成度:
  预期步骤数: 6
  检测步骤数: 4
  完成率: 66.7%

准确性评估:
  正确步骤: 5
  错误步骤: 3
  准确率: 62.5%
```

### 生成文件
- 📸 **问题截图**: `issue_01_t30s.png`
- ✅ **正确示例**: `correct_01_t15s.png`
- 📋 **详细报告**: `analysis_report.json`

## ⚙️ 主要参数调整

### 分析间隔
```python
# 修改关键帧提取间隔（秒）
key_frames = analyzer.extract_key_frames(video_path, interval=15)  # 每15秒一帧
```

### 置信度阈值
```python
# 在 detect_single_component 函数中调整
analyzer.analyze_video(video_path, min_confidence=0.3)  # 最小置信度30%
```

## 🔧 下一步改进

1. **替换模拟检测**：在 `detect_equipment_in_frame()` 中集成真实的设备检测
2. **优化步骤识别**：改进 `identify_experiment_step()` 的判断逻辑
3. **添加更多指标**：扩展评估维度和报告内容

## 💡 提示

- 视频文件支持常见格式：mp4, avi, mov
- 分析速度取决于视频长度和帧率
- 建议先用短视频测试功能
- 可以通过调整 `interval` 参数控制分析精度vs速度的平衡

## 🆘 常见问题

### Q: 找不到视频文件
A: 确保视频文件在正确的路径，并检查文件名是否匹配代码中的设置

### Q: 分析速度太慢
A: 增大 `interval` 参数，减少提取的关键帧数量

### Q: 检测结果不准确
A: 当前使用的是模拟检测，需要集成真实的计算机视觉算法

### Q: 内存不足
A: 处理大视频文件时可能占用较多内存，建议使用较小的测试视频或优化代码
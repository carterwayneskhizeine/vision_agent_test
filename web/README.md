# 迈克尔逊干涉实验AI分析原型

这是一个用于分析迈克尔逊干涉实验教学视频的AI原型系统，能够自动识别实验步骤，对比学生与教师的操作，并生成详细的分析报告。

## 功能特性

### 🎯 核心功能
- **视频分析**: 自动提取关键帧并分析实验内容
- **步骤识别**: 识别6个标准实验步骤的执行情况
- **设备检测**: 检测7种关键实验设备的使用
- **对比分析**: 对比学生操作与标准流程的差异
- **智能报告**: 生成包含截图和建议的详细报告

### 📊 支持的实验步骤
1. **迈克尔逊干涉仪初始设置** (t=8s)
2. **激光器对准和调节** (t=25s)  
3. **获得干涉条纹** (t=45s)
4. **观察等倾干涉图** (t=60s)
5. **精密测量过程** (t=75s)
6. **法布里-珀罗干涉设置** (t=92s)

### 🔬 检测的实验设备
- 氦氖激光器
- 分束器和补偿板
- 动镜 / 定镜
- 精密测微头
- 扩束器
- 二合一观察屏

## 安装与使用

### 1. 环境准备
```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 快速测试
```bash
# 运行测试脚本（会自动创建示例视频）
python test_analyzer.py
```

### 3. 使用真实视频 🎯 **推荐**
```bash
# 准备文件：student.mp4, part1.png-part6.png
# 快速检测模式（提取1分53秒的帧进行设备检测）
python quick_detection.py

# 或者运行完整程序
python experiment_analyzer_prototype.py
```

程序会自动提取student.mp4在1分53秒的帧进行设备检测，避免最后一帧被手挡住！

### 4. 测试和调试工具 🔧
```bash
# 测试中文显示效果
python test_chinese_display.py

# 比较两种检测方法的结果
python compare_detection_methods.py
```

### 5. 编程方式使用
```python
from experiment_analyzer_prototype import MichelsonInterferometerAnalyzer

# 初始化分析器
analyzer = MichelsonInterferometerAnalyzer()

# 分析学生视频（现在使用真实检测）
student_analysis = analyzer.analyze_video('student.mp4', 'student')

# 对比分析
comparison_results = analyzer.compare_student_with_teacher(student_analysis)

# 保存结果（带设备检测可视化）
analyzer.save_analysis_screenshots(comparison_results)
report = analyzer.generate_analysis_report(student_analysis, comparison_results)
```

## 输出结果

### 📸 截图文件
- `analysis_output/issue_XX_tXXs.png` - 问题截图
- `analysis_output/correct_XX_tXXs.png` - 正确示例截图
- `real_video_analysis/` - 真实视频分析截图（带设备检测框）

### 📋 分析报告
- `analysis_report.json` - 详细的JSON格式报告
- 包含完成度、准确率、问题列表、改进建议

### 📊 控制台输出
```
迈克尔逊干涉实验AI分析报告
============================================================
分析时间: 2024-01-15 14:30:25
学生视频: student.mp4
分析帧数: 8

实验完成度:
  预期步骤数: 6
  检测步骤数: 4
  完成率: 66.7%

准确性评估:
  总对比次数: 8
  正确步骤: 5
  错误步骤: 3
  准确率: 62.5%

发现的问题:
  1. [t=30s] 步骤错误: 应该执行 '激光器对准和调节'，但检测到 '未识别步骤'
  2. [t=90s] 时间偏差: 时间点 90s 没有对应的标准步骤

改进建议:
  1. 实验步骤大部分正确，但仍有改进空间
  2. 注意按照正确的顺序执行实验步骤
  3. 建议观看教师示范视频，注意关键操作细节
```

## 技术架构

### 🏗️ 核心组件
- **MichelsonInterferometerAnalyzer**: 主分析类
- **extract_key_frames()**: 视频关键帧提取
- **detect_equipment_in_frame()**: 设备检测（待完善）
- **identify_experiment_step()**: 步骤识别
- **compare_student_with_teacher()**: 对比分析

### 🔧 最新更新 ✅
1. **真实设备检测**: 已集成 `imagetest_batch.py` 的完整检测算法！
2. **多尺度匹配**: 支持不同尺度的鲁棒设备检测
3. **特征点检测**: 使用 SIFT/ORB 进行更准确的匹配
4. **可视化增强**: 截图上显示检测到的设备边界框和置信度
5. **智能文件检查**: 自动验证必需文件并给出友好提示

## 开发路线图

### 🚀 第一阶段（当前）
- [x] 基础视频分析框架
- [x] 步骤定义和时间映射
- [x] 简单的对比分析功能
- [x] 报告生成和可视化

### 🎯 第二阶段（已完成 ✅）
- [x] 集成真实的设备检测算法
- [x] 改进检测的准确性和鲁棒性  
- [x] 增强可视化和报告功能
- [x] 优化用户体验和错误处理

### 🌟 第三阶段（下一步）
- [ ] Web界面开发（Vite + FastAPI）
- [ ] 视频上传和在线预览
- [ ] 实时分析进度显示  
- [ ] 交互式分析报告
- [ ] 手部动作识别
- [ ] 多实验类型支持
- [ ] 云端部署和扩展

## 示例输出

运行测试后会生成以下文件：
```
web/
├── test_output/              # 分析截图
│   ├── issue_01_t30s.png    # 问题截图
│   ├── correct_01_t15s.png  # 正确示例
│   └── ...
├── test_analysis_report.json # 详细报告
├── teacher_sample.mp4        # 示例教师视频
└── student_sample.mp4        # 示例学生视频
```

## 贡献与反馈

这是一个原型系统，欢迎提供反馈和改进建议：

1. **算法改进**: 设备检测、步骤识别的准确性
2. **功能扩展**: 新的分析维度和评估指标  
3. **性能优化**: 视频处理速度和内存使用
4. **用户体验**: 报告格式和交互设计

## 许可证

本项目基于现有的 `video_test.py` 和 `imagetest_batch.py` 代码开发，仅用于教学和研究目的。
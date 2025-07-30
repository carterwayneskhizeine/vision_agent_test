# 项目结构说明

## 📁 文件结构

```
web/
├── experiment_analyzer_prototype.py  # 核心分析引擎
├── test_analyzer.py                  # 测试脚本
├── requirements.txt                  # Python依赖
├── README.md                         # 详细文档
├── QUICK_START.md                   # 快速开始指南
└── PROJECT_STRUCTURE.md             # 本文件
```

## 📄 文件详细说明

### 🧠 核心文件

#### `experiment_analyzer_prototype.py` (21KB)
**主要功能**：迈克尔逊干涉实验AI分析引擎

**核心类**：
- `MichelsonInterferometerAnalyzer`: 主分析器类

**关键方法**：
- `extract_key_frames()`: 提取视频关键帧
- `detect_equipment_in_frame()`: 设备检测（待完善）
- `identify_experiment_step()`: 实验步骤识别
- `compare_student_with_teacher()`: 学生与教师对比分析
- `save_analysis_screenshots()`: 保存分析截图
- `generate_analysis_report()`: 生成详细报告

**预定义数据**：
- 6个标准实验步骤定义
- 7种实验设备映射
- 时间节点和成功标准

#### `test_analyzer.py` (6.2KB)
**主要功能**：测试脚本和示例视频生成器

**核心功能**：
- `create_sample_video()`: 创建模拟实验视频
- `test_analyzer_with_sample_videos()`: 完整测试流程
- 自动生成教师和学生示例视频
- 验证分析功能的完整性

### 📋 配置文件

#### `requirements.txt` (69B)
**依赖包**：
```
opencv-python>=4.5.0    # 视频处理和计算机视觉
numpy>=1.20.0          # 数值计算
matplotlib>=3.3.0      # 图表生成和显示
Pillow>=8.0.0          # 图像处理
```

### 📖 文档文件

#### `README.md` (4.8KB)
**完整项目文档**：
- 功能特性概述
- 技术架构说明
- 安装和使用指南
- 输出结果示例
- 开发路线图

#### `QUICK_START.md` (2.9KB)
**快速入门指南**：
- 5分钟快速体验流程
- 真实视频使用方法
- 参数调整建议
- 常见问题解答

## 🚀 使用流程

### 1. 快速测试
```bash
pip install -r requirements.txt
python test_analyzer.py
```

### 2. 使用真实视频
```bash
# 将 teacher.mp4 和 student.mp4 放入web/目录
python experiment_analyzer_prototype.py
```

### 3. 自定义分析
编辑 `experiment_analyzer_prototype.py` 中的参数和路径

## 📊 输出文件

运行后会生成：
```
web/
├── analysis_output/              # 分析截图目录
│   ├── issue_01_t30s.png        # 问题截图
│   ├── correct_01_t15s.png      # 正确示例
│   └── ...
├── analysis_report.json         # 详细JSON报告
├── teacher_sample.mp4           # 示例教师视频
└── student_sample.mp4           # 示例学生视频
```

## 🔧 关键技术点

### 视频处理
- 使用OpenCV进行视频读取和帧提取
- 支持多种视频格式（mp4, avi, mov等）
- 可配置的帧采样间隔

### 图像分析
- 基于时间的步骤识别
- 模拟设备检测（可扩展为真实检测）
- 多颜色标注和可视化

### 报告生成
- 中文支持的matplotlib图表
- JSON格式的结构化报告
- 自动截图保存和标注

## 🎯 扩展点

### 待完善功能
1. **真实设备检测**：集成 `imagetest_batch.py` 的检测算法
2. **手部动作识别**：识别学生的操作动作
3. **更精确的步骤判断**：基于视觉特征而非仅时间
4. **性能优化**：大视频文件的内存和速度优化

### 未来发展方向
1. **Web界面**：Vite + FastAPI的前后端架构
2. **实时分析**：在线视频流分析
3. **交互式报告**：可视化的分析结果展示
4. **多实验支持**：扩展到其他物理实验

## 💡 设计理念

### 模块化设计
- 核心分析器与界面分离
- 可插拔的检测算法
- 标准化的数据接口

### 可扩展性
- 易于添加新的实验步骤
- 支持不同的检测方法
- 灵活的报告格式

### 用户友好
- 中文界面和报告
- 详细的文档和示例
- 渐进式的学习曲线

这个原型为后续的Web应用开发奠定了坚实的基础！
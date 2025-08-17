# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two main projects for AI-powered analysis of Michelson interferometer physics experiments:

1. **michelsen-web-analyzer/**: Full-stack web application (FastAPI + Vue 3) for video analysis via web interface
2. **web/**: Standalone Python prototype for command-line video analysis and equipment detection

## Development Commands

### Web Application (michelsen-web-analyzer/)

**One-click development startup (recommended):**
```bash
cd michelsen-web-analyzer
python start-dev.py
```

**Manual startup:**
```bash
# Backend only
python start-backend.py

# Frontend only (separate terminal)
node start-frontend.js
```

**Package building:**
```bash
# Build all packages
npm run build
python build-package.py all

# Build specific packages
python build-package.py prod    # Production package
python build-package.py dev     # Development package
python build-executable.py     # Standalone executable
```

**Frontend development:**
```bash
cd frontend
npm install
npm run dev                     # Development server
npm run build                   # Production build
npm run type-check             # TypeScript checking
```

**Backend development:**
```bash
cd backend
pip install -r requirements.txt
python main.py                 # Start FastAPI server
```

### Standalone Prototype (web/)

**Quick analysis modes:**
```bash
cd web
python experiment_analyzer_prototype.py    # Smart analysis (auto-detects files)
python student_operation_analysis.py       # Student operation analysis
python quick_detection.py                  # Equipment detection only
python test_analyzer.py                    # Test with sample data
```

## Architecture

### Web Application Architecture

**Backend (FastAPI):**
- `backend/main.py`: FastAPI application entry point with CORS and static file serving
- `backend/api/routers/`: REST API endpoints for upload and analysis
- `backend/services/`: Business logic for video analysis and AI processing
- `backend/analyzer/`: Core AI analysis engine (same as standalone prototype)
- `backend/core/config.py`: Application configuration and settings

**Frontend (Vue 3 + Vite):**
- `frontend/src/main.ts`: Vue 3 application bootstrap with Pinia and Vue Router
- `frontend/src/views/`: Page components (Home, Analysis)
- `frontend/src/api/`: HTTP client for backend communication
- `frontend/src/types/`: TypeScript type definitions
- Uses DaisyUI + Tailwind CSS for responsive UI components

### AI Analysis Engine

Both projects share the same core analysis engine (`MichelsonInterferometerAnalyzer` class):

**Key capabilities:**
- Video frame extraction and analysis at predefined time points
- Equipment detection using OpenCV and SIFT/ORB feature matching
- Experiment step identification (6 standard steps: setup, laser alignment, interference patterns, measurement, etc.)
- Comparative analysis between teacher demonstration and student videos
- Visual report generation with annotated screenshots

**Detection targets:**
- 7 types of physics equipment: HeNe laser, beam splitter, mirrors, precision micrometer, beam expander, observation screen
- 6 experiment steps with timing validation and accuracy scoring

### File Organization

**Analysis outputs:**
- `backend/static/screenshots/`: Generated analysis screenshots
- `backend/uploads/`: Uploaded video files
- `web/analysis_output/`: Standalone prototype outputs
- `web/real_video_analysis/`: Real video analysis with equipment detection boxes

## Environment Setup

**Required API keys:**
```bash
# Set ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-your-key"

# Or create .env file in backend/ directory
echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key" > backend/.env
```

**Dependencies:**
- Python 3.8+ with OpenCV, NumPy, Matplotlib, FastAPI, Uvicorn
- Node.js 16+ for frontend development
- vision-agent package for enhanced AI capabilities

## Access Points

**Web application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API documentation: http://localhost:8080/docs

**Analysis workflow:**
1. Upload teacher demonstration video (teacher.mp4)
2. Upload student experiment video (student.mp4)
3. Trigger AI analysis via web interface
4. View results with annotated screenshots and comparative analysis

## Key Implementation Notes

- Backend uses thread-based execution for video analysis to prevent blocking
- Frontend implements real-time progress tracking via API polling
- Equipment detection uses template matching with multiple scale levels for robustness
- Chinese language support is configured in matplotlib for report generation
- CORS is configured to allow frontend-backend communication during development
- File uploads are limited to 50MB with MP4/AVI/MOV format support
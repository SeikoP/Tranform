# Transform 3NF - Build & Deployment Guide

## Tổng quan

Dự án hỗ trợ 3 phương thức deployment:
1. **Standalone EXE** - Windows executable
2. **Docker Container** - Cross-platform containerized
3. **Python Runtime** - Direct Python execution

---

## 1. Build Standalone EXE (Windows)

### Ưu điểm:
- ✅ Dễ phân phối cho end-users
- ✅ Không cần cài Python
- ✅ Single file executable
- ✅ Tốt cho desktop users

### Nhược điểm:
- ❌ File size lớn (~150-200MB)
- ❌ Chỉ chạy trên Windows
- ❌ Build time lâu

### Cách build:

```bash
# Cài PyInstaller
pip install pyinstaller

# Build với spec file
pyinstaller build_exe.spec

# Hoặc build trực tiếp
pyinstaller --onefile --windowed --icon=assets/normalization.ico \
    --add-data "qml;qml" --add-data "assets;assets" \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtQml \
    --name Transform3NF main.py

# Output: dist/Transform3NF.exe
```

### Tối ưu size:
```bash
# Sử dụng UPX compression
pip install pyinstaller[encryption]
pyinstaller --onefile --upx-dir=/path/to/upx build_exe.spec
```

---

## 2. Docker Container

### Ưu điểm:
- ✅ Cross-platform (Windows, Linux, Mac)
- ✅ Isolated environment
- ✅ Dễ scale và deploy
- ✅ Tích hợp với databases
- ✅ Tốt cho production/server

### Nhược điểm:
- ❌ Cần Docker installed
- ❌ Phức tạp hơn cho end-users
- ❌ GUI có thể gặp vấn đề

### Cách build:

```bash
# Build image
docker build -t transform3nf:latest .

# Run container
docker run -d \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/exports:/app/exports \
    -p 8080:8080 \
    --name transform3nf \
    transform3nf:latest

# Hoặc dùng docker-compose
docker-compose up -d
```

### Docker với GUI (X11 forwarding):
```bash
# Linux
docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    transform3nf:latest

# Windows (với VcXsrv)
docker run -it \
    -e DISPLAY=host.docker.internal:0 \
    transform3nf:latest
```

---

## 3. Python Runtime

### Ưu điểm:
- ✅ Dễ develop và debug
- ✅ Flexible và customizable
- ✅ File size nhỏ
- ✅ Tốt cho developers

### Nhược điểm:
- ❌ Cần Python installed
- ❌ Dependency management
- ❌ Không phù hợp end-users

### Cách chạy:

```bash
# Tạo virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Chạy app
python main.py
```

### Tạo portable runtime:
```bash
# Sử dụng PyOxidizer
pip install pyoxidizer
pyoxidizer init-config-file
pyoxidizer build
```

---

## Khuyến nghị Deployment

### Cho End Users (Non-technical):
**→ Standalone EXE**
- Đơn giản nhất
- Double-click để chạy
- Không cần setup

### Cho Enterprise/Production:
**→ Docker Container**
- Dễ deploy lên server
- Tích hợp với CI/CD
- Scalable
- Kết nối databases dễ dàng

### Cho Developers:
**→ Python Runtime**
- Dễ modify code
- Fast iteration
- Full control

---

## Build Scripts

### Windows Batch (build_exe.bat):
```batch
@echo off
echo Building Transform 3NF...
pip install pyinstaller
pyinstaller build_exe.spec
echo Build complete! Check dist/ folder
pause
```

### Linux/Mac Shell (build_exe.sh):
```bash
#!/bin/bash
echo "Building Transform 3NF..."
pip install pyinstaller
pyinstaller build_exe.spec
echo "Build complete! Check dist/ folder"
```

### Docker Build Script:
```bash
#!/bin/bash
echo "Building Docker image..."
docker build -t transform3nf:latest .
docker tag transform3nf:latest transform3nf:$(date +%Y%m%d)
echo "Build complete!"
```

---

## Distribution

### EXE Distribution:
1. Build EXE file
2. Tạo installer với Inno Setup hoặc NSIS
3. Upload lên website/GitHub releases
4. Provide download link

### Docker Distribution:
1. Push to Docker Hub:
```bash
docker tag transform3nf:latest username/transform3nf:latest
docker push username/transform3nf:latest
```

2. Hoặc save as tar:
```bash
docker save transform3nf:latest > transform3nf.tar
# Load on another machine:
docker load < transform3nf.tar
```

---

## Performance Optimization

### EXE:
- Exclude unused modules
- Use UPX compression
- Lazy imports
- Strip debug symbols

### Docker:
- Multi-stage builds
- Minimize layers
- Use alpine base images
- Cache dependencies

### Runtime:
- Use virtual environment
- Compile Python files (.pyc)
- Profile and optimize bottlenecks

---

## Kết luận

**Khuyến nghị cho dự án này:**

1. **Development**: Python Runtime
2. **Desktop Users**: Standalone EXE
3. **Server/Production**: Docker Container

Nếu target là **business users** → Build EXE
Nếu target là **enterprise/cloud** → Docker
Nếu target là **developers** → Python Runtime

Có thể cung cấp cả 3 options để users tự chọn!

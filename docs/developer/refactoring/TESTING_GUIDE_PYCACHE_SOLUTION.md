# 🧪 测试指南 - 解决Chrome扩展加载问题

## 🚨 问题描述

Python在运行时会自动生成`__pycache__`目录，这会导致Chrome扩展加载失败，出现以下错误：

```
Cannot load extension with file or directory name __pycache__. 
Filenames starting with "_" are reserved for use by the system.
```

## ✅ 解决方案

我们提供了多种解决方案来确保测试和Chrome扩展加载都能正常工作：

### 方案1：使用测试管理器（推荐）

#### 🚀 快速使用
```bash
# 运行完整测试周期（推荐）
python3 test_manager.py

# 或者使用具体命令
python3 test_manager.py clean    # 仅清理缓存
python3 test_manager.py test     # 仅运行测试
python3 test_manager.py check    # 仅检查Chrome兼容性
```

#### 🔧 功能特性
- ✅ 自动清理`__pycache__`目录和`.pyc`文件
- ✅ 设置`PYTHONDONTWRITEBYTECODE=1`环境变量防止生成缓存
- ✅ 运行测试并捕获输出
- ✅ 检查Chrome扩展兼容性
- ✅ 完整的测试周期管理

### 方案2：使用Shell脚本

```bash
# 运行测试脚本
./run_tests.sh
```

这个脚本会：
1. 清理现有的Python缓存文件
2. 运行测试
3. 再次清理缓存文件

### 方案3：手动清理

```bash
# 清理__pycache__目录
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# 清理.pyc文件
find . -name "*.pyc" -exec rm -f {} + 2>/dev/null

# 设置环境变量防止生成缓存
export PYTHONDONTWRITEBYTECODE=1

# 运行测试
cd tests
python3 test_optimizations.py
```

## 📁 项目结构

```
cursor-client2login/
├── 📄 manifest.json          # Chrome扩展配置
├── 🔧 background.js          # 后台脚本
├── 🎨 popup.html            # 弹出窗口
├── ⚡ popup.js              # 弹出窗口逻辑
├── 📝 content.js            # 内容脚本
├── 🐍 native_host.py        # 原生主机程序
├── 🧪 test_manager.py       # 测试管理器（推荐）
├── 🔧 run_tests.sh          # 测试脚本
├── 📋 tests/                # 测试目录（被.gitignore排除）
│   └── test_optimizations.py
├── 📊 .gitignore            # 包含__pycache__和tests/
└── 📖 TESTING_GUIDE.md      # 本文档
```

## 🎯 最佳实践

### 开发流程
1. **修改代码** → 编辑Python文件
2. **运行测试** → `python3 test_manager.py`
3. **加载扩展** → 在Chrome中加载扩展目录

### 注意事项
- ✅ 始终在测试后清理缓存文件
- ✅ 使用测试管理器确保完整的清理
- ✅ 测试目录已被.gitignore排除
- ✅ 设置环境变量防止生成缓存

### 环境变量设置
```bash
# 防止Python生成.pyc文件
export PYTHONDONTWRITEBYTECODE=1

# 或者在Python脚本中设置
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
```

## 🔍 故障排除

### 问题1：仍然出现__pycache__错误
**解决方案**：
```bash
# 强制清理所有Python缓存
python3 test_manager.py clean
# 或手动清理
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### 问题2：测试无法找到模块
**解决方案**：
确保测试脚本中的路径设置正确：
```python
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
```

### 问题3：权限错误
**解决方案**：
```bash
# 给脚本执行权限
chmod +x run_tests.sh
chmod +x test_manager.py
```

## 📝 .gitignore配置

确保`.gitignore`文件包含以下内容：
```gitignore
# Python相关
__pycache__/
*.py[cod]
*$py.class

# 测试目录（避免Chrome扩展加载时的__pycache__问题）
tests/
```

## 🎉 总结

通过使用测试管理器，你可以：
- ✅ 安全地运行Python测试
- ✅ 自动清理可能导致Chrome加载失败的文件
- ✅ 确保扩展能够正常加载到Chrome中
- ✅ 保持开发和测试的便利性

**推荐工作流程**：
```bash
# 1. 开发代码
vim native_host.py

# 2. 运行测试
python3 test_manager.py

# 3. 加载到Chrome
# 在Chrome中加载扩展目录，不会出现__pycache__错误
```

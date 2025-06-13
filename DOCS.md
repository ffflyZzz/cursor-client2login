# 📚 文档快速导航

## 🚀 快速开始

### 新用户
1. **[📦 安装指南](docs/user/installation.md)** - 5分钟快速安装
2. **[🎯 使用指南](docs/user/usage.md)** - 三种使用方式

### 开发者
1. **[🧪 测试指南](docs/developer/testing.md)** - 解决Chrome兼容性问题
2. **[🏗️ 项目架构](docs/developer/architecture.md)** - 了解模块化设计

## 📋 完整文档

### 👥 用户文档
- [📦 安装指南](docs/user/installation.md) - 安装步骤和系统要求
- [🎯 使用指南](docs/user/usage.md) - 使用方法和多账户管理

### 👨‍💻 开发者文档
- [🏗️ 项目架构](docs/developer/architecture.md) - 模块化架构设计
- [🧪 测试指南](docs/developer/testing.md) - 开发测试和Chrome兼容性
- [🐛 Bug修复记录](docs/developer/bug-fixes.md) - 历史问题解决方案
- [📊 重构文档](docs/developer/refactoring/) - 代码重构记录

### 🔧 故障排除
- [🔍 诊断指南](docs/troubleshooting/diagnose.md) - 问题诊断步骤
- [🛠️ 修复步骤](docs/troubleshooting/fix-steps.md) - 常见问题解决
- [📋 扩展指南](docs/troubleshooting/EXTENSION_GUIDE.md) - Chrome扩展问题

## 🆘 常见问题

### Chrome扩展加载失败
```bash
# 使用智能测试管理器解决__pycache__问题
python3 test_manager.py
```
详见：[🧪 测试指南](docs/developer/testing.md)

### 原生主机连接失败
```bash
# 重新安装并配置扩展ID
python3 install_native_host.py install
python3 update_native_host.py YOUR_EXTENSION_ID
```
详见：[📦 安装指南](docs/user/installation.md)

### 自动读取失败
检查Cursor是否已安装并登录，详见：[🔧 故障排除](docs/troubleshooting/)

---

📖 **完整文档索引**: [docs/README.md](docs/README.md)

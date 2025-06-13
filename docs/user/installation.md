# 📦 安装指南

## 🚀 快速安装

### 步骤1：下载插件
```bash
git clone https://github.com/ffflyZzz/cursor-client2login.git
cd cursor-client2login
```

### 步骤2：安装到Chrome
1. 打开Chrome浏览器
2. 访问 `chrome://extensions/`
3. 开启"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择项目文件夹

### 步骤3：安装原生主机（推荐）
```bash
# macOS/Linux
python3 install_native_host.py install

# Windows
python install_native_host.py install
```

### 步骤4：配置扩展ID
1. 在Chrome扩展页面复制扩展ID
2. 运行配置命令：
```bash
# macOS/Linux
python3 update_native_host.py YOUR_EXTENSION_ID

# Windows
python update_native_host.py YOUR_EXTENSION_ID
```

### 步骤5：重启Chrome
完全重启Chrome浏览器以使原生主机生效。

## 📋 系统要求

- **Chrome浏览器**: 88+
- **Python**: 3.6+
- **操作系统**: Windows、macOS、Linux
- **Cursor**: 已安装并至少登录过一次

## 🔧 验证安装

1. 点击Chrome工具栏中的插件图标
2. 选择"🤖 自动读取"标签
3. 点击"🔍 自动读取Cursor数据"
4. 如果成功，将自动打开Cursor Dashboard

## ❌ 安装问题排除

### 原生主机安装失败
- 确保Python已正确安装
- Windows用户可能需要管理员权限
- 检查扩展ID是否正确配置

### Chrome扩展加载失败
- 确保开启了开发者模式
- 检查项目目录中是否有`__pycache__`目录（如有请删除）
- 验证manifest.json文件完整性

### 自动读取失败
- 确保Cursor已安装并登录过
- 检查文件权限
- 重启Chrome浏览器

## 🗑️ 卸载

### 卸载原生主机
```bash
python3 install_native_host.py uninstall
```

### 卸载Chrome插件
1. 访问 `chrome://extensions/`
2. 找到"Cursor Client2Login"
3. 点击"移除"

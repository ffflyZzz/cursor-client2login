# 🧪 开发测试指南

## 🚨 重要：Chrome扩展兼容性

Python运行时会生成`__pycache__`目录，导致Chrome扩展加载失败：
```
Cannot load extension with file or directory name __pycache__. 
Filenames starting with "_" are reserved for use by the system.
```

## ✅ 解决方案

### 方案1：智能测试管理器（推荐）

```bash
# 运行完整测试周期
python3 test_manager.py

# 或使用具体命令
python3 test_manager.py clean    # 清理缓存
python3 test_manager.py test     # 运行测试
python3 test_manager.py check    # 检查兼容性
```

**功能特性**：
- ✅ 自动清理`__pycache__`目录和`.pyc`文件
- ✅ 设置`PYTHONDONTWRITEBYTECODE=1`环境变量
- ✅ 运行测试并检查Chrome兼容性
- ✅ 完整的测试周期管理

### 方案2：Shell脚本

```bash
./run_tests.sh
```

### 方案3：手动清理

```bash
# 清理缓存文件
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -exec rm -f {} + 2>/dev/null

# 设置环境变量
export PYTHONDONTWRITEBYTECODE=1

# 运行测试
cd tests
python3 test_optimizations.py
```

## 🏗️ 项目架构

### 核心模块（popup.js）
```javascript
├── ErrorHandler        // 统一错误处理
├── LoadingManager      // 加载状态管理
├── DOMManager          // DOM元素管理
├── AppState           // 应用状态管理
├── UIManager          // 用户界面管理
├── NativeHostManager  // 原生主机通信
├── AccountManager     // 账户管理
├── MessageManager     // 消息通信
├── DashboardManager   // 仪表板管理
├── EventManager       // 事件管理
├── FileManager        // 文件管理
├── DataImportManager  // 数据导入管理
└── App               // 应用初始化
```

### 文件结构
```
cursor-client2login/
├── 📄 manifest.json          # Chrome扩展配置
├── 🔧 background.js          # 后台服务脚本
├── 🎨 popup.html            # 弹出窗口页面
├── ⚡ popup.js              # 弹出窗口逻辑（模块化）
├── 📝 content.js            # 内容脚本
├── 🐍 native_host.py        # 原生主机程序
├── 🧪 test_manager.py       # 测试管理器
├── 🔧 run_tests.sh          # 测试脚本
├── 📋 tests/                # 测试目录
│   └── test_optimizations.py
└── 📚 docs/                 # 文档目录
```

## 🧪 本地测试环境

### 启动测试环境
```bash
# 启动本地服务器
python3 -m http.server 8000

# 访问测试页面
http://localhost:8000/test_refactored.html
```

### 测试功能
- ✅ DOM管理器功能测试
- ✅ UI管理器消息显示测试
- ✅ 加载状态管理测试
- ✅ 错误处理机制测试
- ✅ 应用状态管理测试
- ✅ 调试功能可用性测试

### Chrome API模拟
测试环境完整模拟了Chrome扩展API：
- `chrome.runtime.sendMessage` - 消息通信
- `chrome.runtime.sendNativeMessage` - 原生主机通信
- `chrome.storage.local` - 本地存储
- 错误处理和回调机制

## 🔧 开发工作流程

### 推荐流程
```bash
# 1. 修改代码
vim popup.js

# 2. 运行测试（自动清理缓存）
python3 test_manager.py

# 3. 加载到Chrome（无__pycache__问题）
# 在Chrome中加载扩展目录
```

### 调试技巧
- 使用浏览器开发者工具查看详细日志
- 利用断点调试复杂逻辑
- 通过调试接口实时查看状态
- 模拟不同的错误场景

### 调试接口
```javascript
// 测试账户操作功能
window.testAccountActions();

// 调试Cookie状态
window.debugCookieStatus();

// 查看应用状态
window.AppState.getState();

// 访问核心管理器
window.AccountManager;
window.UIManager;
```

## 📝 代码规范

### 错误处理模式
```javascript
// 推荐的Chrome API调用模式
if (!chrome?.api?.method) {
    console.warn('⚠️ API不可用，可能在测试环境中');
    return fallbackBehavior();
}
```

### 环境检测
```javascript
// 智能环境检测
const isTestEnvironment = !chrome?.runtime?.id;
if (isTestEnvironment) {
    // 提供模拟行为
}
```

## 🎯 最佳实践

1. **防御性编程**: 所有Chrome API调用都检查存在性
2. **环境感知**: 代码能智能检测运行环境
3. **优雅降级**: API不可用时提供合理默认行为
4. **测试隔离**: 使用独立测试目录避免污染扩展

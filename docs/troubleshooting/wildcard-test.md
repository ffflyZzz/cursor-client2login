# 🧪 通配符扩展ID测试

## 🎯 测试目标
验证原生主机配置使用通配符 `chrome-extension://*/` 是否能正常工作

## 📋 当前配置状态
- **原生主机配置**: 通配符模式 `chrome-extension://*/`
- **扩展ID**: `abcdefghijklmnopqrstuvwxyz123456`
- **Chrome状态**: 已重启（配置生效）

## 🧪 测试步骤

### 1. 重新启动Chrome浏览器
确保新的通配符配置已加载

### 2. 测试自动读取功能
1. 打开Cursor Client2Login扩展
2. 点击"🔍 自动读取Cursor数据"按钮
3. 观察结果

### 3. 预期结果对比

#### ✅ 成功情况：
- 显示"自动读取成功！"
- 表单自动填充email、userid、accessToken
- 数据保存并设置Cookie成功

#### ❌ 失败情况：
- 显示错误信息（观察是否与之前不同）
- 查看是否还是"找不到原生主机程序"

## 🔍 调试信息收集

如果测试失败，请收集以下信息：

1. **错误消息**: 记录插件显示的具体错误
2. **Console日志**: 
   - 右键点击扩展图标
   - 选择"检查弹出内容"
   - 查看Console标签页的错误信息

## 📊 测试记录

### 具体扩展ID模式 (之前测试)
- **配置**: `chrome-extension://abcdefghijklmnopqrstuvwxyz123456/`
- **结果**: [待记录]

### 通配符模式 (当前测试)
- **配置**: `chrome-extension://*/`  
- **结果**: [待测试]

## 🔄 快速切换回具体ID
如果通配符模式失败，可以快速切换回具体扩展ID：
```bash
python3 update_native_host.py abcdefghijklmnopqrstuvwxyz123456
```

## 💡 技术说明
- Chrome的原生消息传递API对通配符支持可能因版本而异
- 某些Chrome版本可能要求具体的扩展ID
- 通配符模式理论上应该工作，但实际支持情况需要测试验证

请重新启动Chrome并进行测试！🚀 
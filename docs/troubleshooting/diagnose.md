# Chrome扩展原生主机连接问题诊断

## 当前状态
✅ 原生主机程序工作正常 - 可以成功读取Cursor数据  
❌ Chrome扩展无法连接到原生主机

## 解决步骤

### 1. 🔄 重启Chrome浏览器（最重要）
原生主机配置更改后，必须完全关闭并重新启动Chrome浏览器。

**步骤：**
1. 完全关闭Chrome（确保没有后台进程）
2. 重新启动Chrome
3. 重新测试插件

### 2. 📋 获取准确的扩展ID
通配符(`chrome-extension://*/`)可能不被支持，需要使用具体的扩展ID。

**步骤：**
1. 在Chrome中打开 `chrome://extensions/`
2. 找到"Cursor Client2Login"扩展
3. 复制扩展ID（类似：`abcdefghijklmnopqrstuvwxyz123456`）
4. 运行命令：`python3 update_native_host.py <扩展ID>`

### 3. 🔍 检查权限
确保原生主机文件有执行权限：
```bash
chmod +x /Users/user/python/cursor-local-login/native_host.py
```

### 4. 🧪 测试连接
重启Chrome后，打开扩展，点击"自动读取"按钮，查看是否有详细的错误信息。

### 5. 📝 查看Chrome扩展控制台
1. 右键点击扩展图标
2. 选择"检查弹出内容"
3. 在开发者工具中查看Console标签页的错误信息

## 原生主机测试确认
✅ 原生主机程序可以正确读取到：
- Email: user@example.com
- UserID: user_01xxxxxx
- AccessToken: 有效的JWT令牌

## 常见问题
1. **"Specified native messaging host not found"** - 需要重启Chrome
2. **"Access denied"** - 检查文件权限
3. **连接超时** - 使用具体扩展ID替换通配符

如果按照上述步骤仍然无法解决，请查看Chrome扩展的详细错误日志。 
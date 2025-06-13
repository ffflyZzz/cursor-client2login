# 🎯 使用指南

## 🚀 三种使用方式

### 方式一：🤖 自动读取（推荐）

**优势**：完全自动化，无需手动操作

1. 确保已安装原生主机程序
2. 点击"🔍 自动读取Cursor数据"
3. 等待自动提取和设置完成

插件将自动：
- 读取Cursor数据库获取accessToken
- 解析scope_v3.json获取email和userid
- 设置Cookie和保存到本地存储
- 打开Cursor Dashboard

### 方式二：📁 文件上传

**适用场景**：无法安装原生主机或权限受限

1. 找到配置文件：
   - **macOS**: `~/Library/Application Support/Cursor/sentry/scope_v3.json`
   - **Windows**: `%APPDATA%\Cursor\sentry\scope_v3.json`
2. 拖拽文件到上传区域
3. 手动输入Access Token
4. 点击"📋 处理文件数据"

### 方式三：✋ 手动输入

**适用场景**：需要精确控制或调试

#### 获取所需数据

**获取AccessToken**：
1. 找到数据库文件：
   - **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
   - **Windows**: `%APPDATA%\Cursor\User\globalStorage\state.vscdb`
   - **Linux**: `~/.config/Cursor/User/globalStorage/state.vscdb`

2. 使用SQLite工具查询：
   ```sql
   SELECT value FROM itemTable WHERE key = 'cursorAuth/accessToken';
   ```

**获取Email和UserID**：
1. 打开scope_v3.json文件
2. 找到以下结构：
   ```json
   {
     "scope": {
       "user": {
         "email": "your-email@example.com",
         "id": "auth0|user_01XXXXXXXXX"
       }
     }
   }
   ```
3. 提取email和id中"|"后面的部分作为userid

#### 快速获取命令
在项目目录下执行：
```bash
python3 - <<'PY'
from native_host import CursorDataManager
import json, sys
token = CursorDataManager.read_access_token()
scope = CursorDataManager.read_scope_json()
if "error" in token: sys.exit(f"❌ {token['error']}")
if "error" in scope: sys.exit(f"❌ {scope['error']}")
print(json.dumps({
    "email": scope["email"],
    "userid": scope["userid"],
    "accessToken": token["accessToken"][:10] + "..."
}, ensure_ascii=False, indent=2))
PY
```

## 🔄 多账户管理

### 添加账户
使用任意方式导入新的Cursor账户，所有账户都会自动保存

### 快速切换

#### 插件内切换
- 在"已保存的账户"列表中点击"切换"按钮

#### 网站内切换
1. 访问任何 cursor.com 页面
2. 点击右上角的 🎯 浮动按钮
3. 选择要切换的账户
4. 页面自动刷新并应用新认证

## 🛡️ 安全说明

- ✅ **本地处理** - 所有认证数据仅在本地处理
- ✅ **无服务器通信** - 不会发送数据到任何外部服务器
- ✅ **权限最小化** - 仅请求必要的浏览器权限
- ✅ **开源透明** - 完全开源，代码透明可审计

**安全建议**：
- 定期更新AccessToken确保安全性
- 如怀疑账户安全，请及时更改Cursor密码
- 妥善保管AccessToken等敏感信息

## 🔧 Cookie格式说明

插件会自动将userid和accessToken拼接成以下格式：
```
userid%3A%3AaccessToken
```
这个值会被设置为名为 `WorkosCursorSessionToken` 的Cookie。

## 📊 数据存储

- 所有账户信息都保存在Chrome的本地存储中
- 不会上传到任何服务器
- 可以随时清空所有数据

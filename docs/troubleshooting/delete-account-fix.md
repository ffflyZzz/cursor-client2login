# 🗑️ 删除账户功能完善

## 🎯 问题描述
删除当前正在使用的账户时，只从账户列表中移除了账户，但没有清理相关的：
- Cookie（WorkosCursorSessionToken）
- currentAccount 本地存储数据

## ✅ 修复内容

### 1. 🔍 智能检测当前账户
在删除账户时，会比较要删除的账户与 `currentAccount` 的：
- Email 地址
- User ID

### 2. 🧹 完整数据清理
如果删除的是当前账户，会自动：

#### a) 清除本地存储
```javascript
await chrome.storage.local.remove(['currentAccount']);
```

#### b) 清除 Cursor 认证 Cookie
- 主要清除：`WorkosCursorSessionToken`
- 扫描清除：所有包含 `session`、`auth`、`token` 的相关 Cookie
- 覆盖域名：`.cursor.com` 下的所有相关 Cookie

### 3. 📋 详细日志记录
删除过程中的每个步骤都有详细日志：
- 🗑️ 删除请求信息
- 🔍 当前账户检测结果  
- 🧹 数据清理过程
- ✅ 操作完成确认

### 4. 💬 用户友好提示
- **普通账户删除**：`已删除账户: user@example.com`
- **当前账户删除**：`已删除当前账户: user@example.com\n相关Cookie和数据已清理`

## 🔧 技术实现

### popup.js 修改
```javascript
// 检查是否为当前账户
const isCurrentAccount = currentAccount && 
                        currentAccount.email === deletedAccount.email && 
                        currentAccount.userid === deletedAccount.userid;

if (isCurrentAccount) {
    // 清除本地数据
    await chrome.storage.local.remove(['currentAccount']);
    
    // 清除Cookie
    const clearCookieResult = await sendMessage('clearCookie');
}
```

### background.js 新增
```javascript
// 新增消息处理
} else if (request.action === 'clearCookie') {
  clearCursorCookie().then(sendResponse);
  return true;

// 新增清除Cookie函数
async function clearCursorCookie() {
  // 清除主要Cookie
  await chrome.cookies.remove({
    url: 'https://www.cursor.com',
    name: 'WorkosCursorSessionToken'
  });
  
  // 扫描清除相关Cookie
  const allCookies = await chrome.cookies.getAll({domain: '.cursor.com'});
  // ... 清理逻辑
}
```

## 🧪 测试步骤

1. **添加多个账户**到插件中
2. **切换到某个账户**（确保它成为 currentAccount）
3. **删除该账户**
4. **检查结果**：
   - 账户列表中已移除
   - currentAccount 已清空
   - Cookie 已清除
   - 提示信息显示"相关Cookie和数据已清理"

## 🔍 调试信息

删除过程中可在控制台看到：
```
🗑️ 删除账户请求，索引: 0
📋 当前账户列表: [...]
🧹 删除的是当前账户，开始清理相关数据...
✅ currentAccount 已清除
🍪 开始清除Cursor认证Cookie...
✅ WorkosCursorSessionToken Cookie已清除
✅ 账户列表已刷新
```

## 🎉 功能优势

1. **数据一致性**：确保删除账户时相关数据完全清理
2. **安全性**：防止已删除账户的认证信息残留
3. **用户体验**：自动处理，无需手动清理
4. **智能判断**：只在删除当前账户时清理，避免误操作

现在删除账户功能更加完善和安全！🛡️ 
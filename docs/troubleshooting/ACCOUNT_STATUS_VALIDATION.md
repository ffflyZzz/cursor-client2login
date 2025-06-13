# 🔍 账户状态验证功能

## 问题背景

在之前的实现中，当前账户的显示仅基于 `chrome.storage.local` 中的 `currentAccount` 数据，这可能导致显示的账户与实际生效的账户不一致的问题：

- **显示的账户**：基于 storage 中的 `currentAccount`
- **实际生效的账户**：基于 Cookie 中的 `WorkosCursorSessionToken`

这种不一致可能发生在以下情况：
1. Cookie 已过期但 storage 中仍有账户信息
2. Cookie 被手动清除但 storage 未更新
3. 用户在外部切换了账户但插件未感知
4. storage 和 Cookie 中的账户 ID 不匹配

## 🎯 解决方案

### 新增功能

#### 1. Cookie 状态检查 (`getCurrentCookieStatus`)
- 检查 `WorkosCursorSessionToken` Cookie 是否存在
- 解析 Cookie 中的 `userid` 和 `accessToken`
- 验证 Cookie 是否过期
- 返回详细的 Cookie 状态信息

#### 2. 账户状态验证 (`validateCurrentAccountStatus`)
- 对比 storage 和 Cookie 中的账户信息
- 判断两者是否一致
- 提供具体的状态建议

#### 3. 智能状态显示
根据验证结果显示不同的状态：

**✅ 正常状态** - storage 和 Cookie 一致
```
✅ 当前账户
user@example.com
user123456
状态正常
```

**⚠️ 警告状态** - 基于 Cookie 识别
```
⚠️ 当前账户
user@example.com
user123456
基于Cookie识别
```

**🔄 需要重新切换** - Cookie 无效
```
🔄 当前账户
user@example.com
user123456
请重新切换
```

**⏰ Cookie 过期**
```
⏰ 当前账户
user@example.com
user123456
Cookie已过期
```

**🍪 Cookie 清除**
```
🍪 当前账户
user@example.com
user123456
Cookie已清除
```

## 🛠️ 技术实现

### Background Script 新增 API

```javascript
// 获取 Cookie 状态
chrome.runtime.sendMessage({
  action: 'getCurrentCookieStatus'
}, (response) => {
  console.log('Cookie状态:', response);
});

// 验证账户状态
chrome.runtime.sendMessage({
  action: 'validateCurrentAccountStatus'
}, (response) => {
  console.log('验证结果:', response.status);
});
```

### 状态响应格式

#### getCurrentCookieStatus 响应
```javascript
{
  success: true,
  hasCookie: true,
  cookieData: {
    userid: "user123456",
    accessToken: "token...",
    expirationDate: 1234567890,
    isExpired: false,
    domain: ".cursor.com",
    path: "/"
  },
  message: "Cookie有效"
}
```

#### validateCurrentAccountStatus 响应
```javascript
{
  success: true,
  status: {
    isConsistent: true,
    storageAccount: {...},
    cookieStatus: {...},
    recommendation: "当前账户状态正常"
  }
}
```

## 🎨 用户体验改进

### 1. 视觉反馈
- **绿色边框** - 状态正常
- **橙色边框** - 需要注意的状态
- **灰色边框** - 无账户状态

### 2. 状态说明
每个状态都会显示简短的说明，帮助用户理解当前情况

### 3. 手动验证
添加了"🔍 验证账户状态"按钮，用户可以手动触发状态检查

## 🔧 使用场景

### 场景 1：Cookie 过期
- **现象**：用户发现无法访问 Cursor Dashboard
- **显示**：⏰ Cookie已过期
- **建议**：点击当前账户的"切换"按钮重新设置 Cookie

### 场景 2：外部账户切换
- **现象**：用户在 Cursor 网页版切换了账户
- **显示**：⚠️ 基于Cookie识别 或显示"未知账户"
- **建议**：导入新账户或切换到正确的账户

### 场景 3：Cookie 被清除
- **现象**：浏览器清除了 Cookie
- **显示**：🍪 Cookie已清除
- **建议**：重新切换到该账户

### 场景 4：数据不一致
- **现象**：storage 和 Cookie 中的账户不匹配
- **显示**：⚠️ 数据不一致
- **建议**：重新切换账户以同步数据

## 🚀 优势

1. **准确性**：显示真实生效的账户状态
2. **透明性**：用户清楚知道当前的认证状态
3. **可诊断**：提供具体的问题说明和解决建议
4. **自动化**：每次打开插件都会自动验证状态
5. **灵活性**：支持手动验证和状态刷新

## 📋 测试建议

1. **正常场景测试**
   - 导入账户并切换
   - 验证状态显示为"✅ 状态正常"

2. **Cookie 过期测试**
   - 手动清除 Cookie
   - 验证状态显示为"🍪 Cookie已清除"

3. **不一致测试**
   - 在外部切换账户
   - 验证状态能够检测到不一致

4. **恢复测试**
   - 在异常状态下点击"切换"按钮
   - 验证状态恢复正常

这个功能大大提高了插件的可靠性和用户体验，确保用户始终了解真实的账户状态。 
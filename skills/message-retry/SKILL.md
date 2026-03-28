# Message Retry - 消息发送重试机制

## 用途

确保 WhatsApp 消息可靠发送，自动检测发送失败并重试。

## 触发条件

- 用户明确要求消息必须发送成功
- 检测到 WhatsApp 连接不稳定
- 重要通知类消息（告警、提醒等）

## 重试策略

### 1. 发送前检查
```bash
# 检查 WhatsApp 连接状态
openclaw gateway status
# 或查看最近日志确认连接状态
```

### 2. 发送并确认
```bash
# 发送消息
message action=send channel=whatsapp target=<号码> message="<内容>"

# 检查返回结果：
# - 成功：返回 messageId (如 3EB0F18F984377631B494D)
# - 失败：返回错误信息
```

### 3. 失败重试逻辑
```
最大重试次数：3 次
重试间隔：5 秒 → 10 秒 → 30 秒（指数退避）

如果 3 次后仍失败：
  1. 检查 WhatsApp 连接状态
  2. 如断开，等待自动重连或手动重连
  3. 重连成功后再次尝试发送
  4. 发送告警通知用户
```

### 4. 发送确认流程
```
1. 发送消息 → 获取 messageId
2. 等待 10-30 秒
3. 检查消息状态（如平台支持）
4. 如失败，触发重试
```

## 使用示例

### 简单发送（自动重试）
```bash
# 发送重要消息，带重试
message action=send channel=whatsapp target=+8613370822913 \
  message="⚠️ 重要通知：..." \
  bestEffort=false
```

### 手动重试流程
```bash
# 第一次发送
result=$(message action=send channel=whatsapp target=+8613370822913 message="测试")

# 检查是否成功
if echo "$result" | grep -q "messageId"; then
  echo "发送成功"
else
  echo "发送失败，5 秒后重试..."
  sleep 5
  # 重试...
fi
```

## 日志记录

每次发送后记录到 `memory/YYYY-MM-DD.md`:
```markdown
### 消息发送记录
- 时间：HH:MM:SS
- 目标：+8613370822913
- 状态：成功/失败
- messageId: 3EB0...
- 重试次数：0/1/2/3
```

## 注意事项

1. **不要无限重试** - 最多 3 次，避免刷屏
2. **区分错误类型** - 网络错误可重试，认证错误需重新登录
3. **重要消息优先** - 告警类消息优先级最高
4. **记录完整日志** - 便于追踪问题

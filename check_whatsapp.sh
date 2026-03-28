#!/bin/bash
# WhatsApp Gateway 状态检查脚本
# 用途：检查 Gateway 连接状态，断连时发送提醒
# 使用方法：添加到 crontab 定期运行（如：*/5 * * * * /path/to/check_whatsapp.sh）

GATEWAY_URL="http://127.0.0.1:18789"
ADMIN_NUMBER="+8613370822913"
STATE_FILE="$HOME/.openclaw/workspace/whatsapp_last_state.txt"
ALERT_COOLDOWN_FILE="$HOME/.openclaw/workspace/whatsapp_last_alert.txt"
COOLDOWN_SECONDS=300  # 5分钟冷却

# 获取当前时间戳
NOW=$(date +%s)

# 检查 Gateway 状态
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$GATEWAY_URL/health" 2>/dev/null || echo "000")

# 判断状态
if [ "$HTTP_CODE" = "200" ]; then
    CURRENT_STATUS="connected"
else
    CURRENT_STATUS="disconnected"
fi

# 读取上次状态
if [ -f "$STATE_FILE" ]; then
    LAST_STATUS=$(cat "$STATE_FILE")
else
    LAST_STATUS="unknown"
fi

# 输出状态
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Gateway 状态: $CURRENT_STATUS (HTTP $HTTP_CODE)" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log"

# 检测状态变化到断连
if [ "$CURRENT_STATUS" = "disconnected" ] && [ "$LAST_STATUS" != "disconnected" ]; then
    # 检查冷却时间
    if [ -f "$ALERT_COOLDOWN_FILE" ]; then
        LAST_ALERT=$(cat "$ALERT_COOLDOWN_FILE")
        ELAPSED=$((NOW - LAST_ALERT))
    else
        ELAPSED=$((COOLDOWN_SECONDS + 1))
    fi

    if [ $ELAPSED -ge $COOLDOWN_SECONDS ]; then
        # 发送提醒
        ALERT_MSG="⚠️ WhatsApp Gateway 断连！

时间: $(date '+%Y-%m-%d %H:%M:%S')
HTTP 状态码: $HTTP_CODE

运行以下命令重启:
openclaw gateway restart"

        # 发送消息（通过 message 工具）
        echo "$ALERT_MSG" | message send --channel whatsapp --to "$ADMIN_NUMBER" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log" 2>&1

        # 记录提醒时间
        echo "$NOW" > "$ALERT_COOLDOWN_FILE"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ 提醒已发送" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log"
    else
        REMAINING=$((COOLDOWN_SECONDS - ELAPSED))
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] → 跳过提醒（冷却中，还剩${REMAINING}秒）" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log"
    fi
elif [ "$CURRENT_STATUS" = "connected" ] && [ "$LAST_STATUS" = "disconnected" ]; then
    # 恢复提醒
    ALERT_MSG="✅ WhatsApp Gateway 已恢复连接！

时间: $(date '+%Y-%m-%d %H:%M:%S')"

    echo "$ALERT_MSG" | message send --channel whatsapp --to "$ADMIN_NUMBER" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ 恢复提醒已发送" >> "$HOME/.openclaw/workspace/whatsapp_monitor.log"
fi

# 更新状态文件
echo "$CURRENT_STATUS" > "$STATE_FILE"

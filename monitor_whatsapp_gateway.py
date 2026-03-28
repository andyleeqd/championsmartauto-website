#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控 WhatsApp Gateway 连接状态
断连时自动发送提醒
"""

import requests
import time
import json
import subprocess
from datetime import datetime

# 配置
GATEWAY_URL = "http://127.0.0.1:18789"
CHECK_INTERVAL = 60  # 检查间隔（秒）
ALERT_COOLDOWN = 300  # 提醒冷却时间（秒，5分钟内不重复提醒）
ADMIN_NUMBER = "+8613370822913"  # 管理员号码

# 状态跟踪
last_alert_time = 0
last_status = "unknown"

def check_gateway_status():
    """检查 Gateway 状态"""
    try:
        response = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return "connected", data
        else:
            return f"error_{response.status_code}", None
    except requests.exceptions.RequestException as e:
        return "disconnected", str(e)

def send_alert(message):
    """发送提醒消息"""
    try:
        # 使用 message 工具发送
        result = subprocess.run([
            "message", "send",
            "--channel", "whatsapp",
            "--to", ADMIN_NUMBER,
            "--message", message
        ], capture_output=True, text=True, timeout=10)
        print(f"[✓] 提醒已发送: {message}")
        return True
    except Exception as e:
        print(f"[✗] 发送提醒失败: {e}")
        return False

def main():
    global last_alert_time, last_status

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始监控 WhatsApp Gateway...")
    print(f"检查间隔: {CHECK_INTERVAL}秒, 提醒冷却: {ALERT_COOLDOWN}秒")
    print(f"管理员: {ADMIN_NUMBER}")
    print("-" * 50)

    while True:
        current_time = time.time()
        status, data = check_gateway_status()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_icon = "✓" if status == "connected" else "✗"

        print(f"[{timestamp}] [{status_icon}] 状态: {status}")

        # 检测状态变化
        if status == "disconnected" and last_status != "disconnected":
            # 检查冷却时间
            if current_time - last_alert_time >= ALERT_COOLDOWN:
                alert_msg = f"⚠️ WhatsApp Gateway 断连！\n\n时间: {timestamp}\n错误: {data}\n\n运行以下命令重启:\nopenclaw gateway restart"
                send_alert(alert_msg)
                last_alert_time = current_time
            else:
                print(f"  → 跳过提醒（冷却中，还剩{int(ALERT_COOLDOWN - (current_time - last_alert_time))}秒）")
        elif status == "connected" and last_status == "disconnected":
            # 恢复提醒
            alert_msg = f"✅ WhatsApp Gateway 已恢复连接\n\n时间: {timestamp}"
            send_alert(alert_msg)

        last_status = status
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 监控已停止")
    except Exception as e:
        print(f"[错误] {e}")
        raise

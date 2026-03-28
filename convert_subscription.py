#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订阅链接转换工具
支持: txt/v2ray/ssr 转换为 Clash yaml
"""

import requests
import sys

def convert_subscription(sub_url, target="clash"):
    """
    转换订阅链接

    Args:
        sub_url: 原订阅链接
        target: 目标格式 (clash/clashmeta/v2ray/singbox/quantumultx)

    Returns:
        转换后的订阅链接和内容
    """
    # 使用 subconverter API
    api_url = f"https://sub.xeton.dev/sub"
    params = {
        "target": target,
        "url": sub_url,
        "new_name": "converted"
    }

    try:
        print(f"正在转换订阅链接...")
        print(f"目标格式: {target}")
        response = requests.post(api_url, data=params, timeout=30)

        if response.status_code == 200:
            print("✅ 转换成功！")
            return response.text
        else:
            print(f"❌ 转换失败: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def save_to_file(content, filename):
    """保存内容到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已保存到: {filename}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <订阅链接> [目标格式]")
        print(f"\n目标格式选项:")
        print("  clash      - Clash (默认)")
        print("  clashmeta  - Clash Meta")
        print("  v2ray      - V2Ray")
        print("  singbox    - Sing-box")
        print("  quantumultx - QuantumultX")
        print("\n示例:")
        print(f"  python3 {sys.argv[0]} 'https://example.com/sub.txt' clash")
        print(f"  python3 {sys.argv[0]} 'https://example.com/sub.txt'")
        sys.exit(1)

    sub_url = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "clash"

    # 转换
    result = convert_subscription(sub_url, target)

    if result:
        # 保存到文件
        filename = f"converted_{target}.yaml"
        save_to_file(result, filename)

        print(f"\n✅ 转换完成！")
        print(f"📁 文件: {filename}")
        print(f"\n也可以使用以下 API 直接获取:")
        print(f"https://sub.xeton.dev/sub?target={target}&url={sub_url}")

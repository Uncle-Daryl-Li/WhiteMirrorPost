#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试前后端连接"""

import time
import requests

def test_health():
    """测试健康检查端点"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"[OK] 健康检查成功")
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.text}")
        return True
    except Exception as e:
        print(f"[FAIL] 健康检查失败: {e}")
        return False

def test_generate_simple():
    """测试简单生成请求"""
    try:
        data = {
            "prompt": "测试海报",
            "aspect_ratio": "9:16",
            "count": 1,
            "preset_style": "Auto",
            "style_intensity": 0.5,
            "thinking_mode": False  # 使用快速模式测试
        }

        print("\n发送测试请求...")
        response = requests.post(
            'http://localhost:8000/api/generate',
            json=data,
            timeout=60
        )

        print(f"[OK] 生成请求成功")
        print(f"  状态码: {response.status_code}")
        result = response.json()
        print(f"  成功: {result.get('success')}")
        print(f"  消息: {result.get('message')}")
        print(f"  图片数量: {len(result.get('images', []))}")
        return True

    except Exception as e:
        print(f"[FAIL] 生成请求失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("MirrorPost AI - 前后端连接测试")
    print("=" * 50)

    # 等待服务器完全启动
    print("\n等待服务器启动...")
    time.sleep(2)

    # 测试健康检查
    print("\n[1/2] 测试健康检查端点")
    health_ok = test_health()

    if not health_ok:
        print("\n[WARNING] 后端服务器未响应，请确保:")
        print("  1. 运行 python server.py")
        print("  2. 检查端口8000未被占用")
        exit(1)

    # 测试生成API（可选，因为需要API Key）
    print("\n[2/2] 测试生成API（可选）")
    print("注意: 此测试需要有效的GOOGLE_API_KEY")
    choice = input("是否测试生成API? (y/n): ")

    if choice.lower() == 'y':
        test_generate_simple()
    else:
        print("跳过生成API测试")

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)

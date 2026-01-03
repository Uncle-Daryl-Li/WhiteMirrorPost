#!/usr/bin/env python
# 测试更新后的 API

import requests
import json

# 测试请求数据（不包含图片素材）
test_data = {
    "prompt": "测试海报生成",
    "aspect_ratio": "9:16",
    "count": 1,
    "preset_style": "Auto",
    "style_intensity": 0.5,
    "negative_prompt": None,
    "thinking_mode": True,
    "reference_image": None,
    "logo_image": None,
    "qrcode_image": None,
    "combo_images": None
}

print("发送测试请求到 http://localhost:8000/api/generate")
print(f"请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
print("\n" + "="*50 + "\n")

try:
    response = requests.post(
        "http://localhost:8000/api/generate",
        json=test_data,
        timeout=60
    )

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        print("✅ API 请求成功!")
        data = response.json()
        print(f"生成了 {len(data.get('images', []))} 张图片")
    else:
        print(f"❌ API 返回错误: {response.status_code}")
        print(f"错误详情: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ 无法连接到后端服务器")
    print("请确保运行了: python server.py")
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")

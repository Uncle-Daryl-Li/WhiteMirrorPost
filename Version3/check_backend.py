#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 检查后端配置是否正确

import sys
import inspect

print("="*60)
print("  Backend Configuration Check")
print("="*60)

# 1. 检查 backend.py
print("\n[1] Checking backend.py...")
try:
    from backend import generate_posters

    # 获取函数签名
    sig = inspect.signature(generate_posters)
    params = list(sig.parameters.keys())

    print(f"[OK] backend.py imported successfully")
    print(f"     Function parameters: {', '.join(params)}")

    # 检查是否包含新参数
    required_params = ['combo_images']
    missing = [p for p in required_params if p not in params]

    if missing:
        print(f"[ERROR] Missing parameters: {', '.join(missing)}")
        print("        Need to reload backend.py")
    else:
        print(f"[OK] All required parameters present")

except Exception as e:
    print(f"[ERROR] backend.py import failed: {str(e)}")
    sys.exit(1)

# 2. 检查 server.py
print("\n[2] Checking server.py...")
try:
    from server import GenerateRequest

    # 获取模型字段
    fields = GenerateRequest.model_fields
    field_names = list(fields.keys())

    print(f"[OK] server.py imported successfully")
    print(f"     GenerateRequest fields: {', '.join(field_names)}")

    # 检查是否包含新字段
    required_fields = ['logo_image', 'qrcode_image', 'combo_images']
    missing = [f for f in required_fields if f not in field_names]

    if missing:
        print(f"[ERROR] Missing fields: {', '.join(missing)}")
        print("        Need to reload server.py")
    else:
        print(f"[OK] All required fields present")

except Exception as e:
    print(f"[ERROR] server.py import failed: {str(e)}")
    sys.exit(1)

# 3. 检查环境变量
print("\n[3] Checking environment variables...")
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print(f"[OK] GOOGLE_API_KEY is set (length: {len(api_key)})")
else:
    print(f"[ERROR] GOOGLE_API_KEY is not set")
    print("        Please set GOOGLE_API_KEY in .env file")

print("\n" + "="*60)
print("  Check Complete")
print("="*60)
print("\nIf all checks pass, run: python server.py")

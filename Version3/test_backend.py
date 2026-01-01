#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick Backend Test"""

import requests
import sys

print("=" * 60)
print("  Testing Backend Connection")
print("=" * 60)
print()

print("[Test 1] Checking if backend is accessible...")
try:
    response = requests.get('http://localhost:8000/', timeout=3)
    print(f"✓ SUCCESS! Backend is running!")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    print()
    print("=" * 60)
    print("  Backend is OK! The problem might be elsewhere.")
    print("=" * 60)
except requests.exceptions.ConnectionError:
    print("✗ FAILED! Backend is NOT running!")
    print()
    print("=" * 60)
    print("  SOLUTION:")
    print("=" * 60)
    print()
    print("  The backend server is NOT running.")
    print("  You need to start it first!")
    print()
    print("  Option 1 - Use the start script:")
    print("    1. Close all windows")
    print("    2. Double click: start.bat")
    print()
    print("  Option 2 - Start backend manually:")
    print("    1. Open a NEW Command Prompt window")
    print("    2. cd D:\\WhiteMirror\\Post\\Version3")
    print("    3. python server.py")
    print("    4. Keep the window OPEN")
    print()
    print("=" * 60)
    sys.exit(1)
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

print()
input("Press Enter to exit...")

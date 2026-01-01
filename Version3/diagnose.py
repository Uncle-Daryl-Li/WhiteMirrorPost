#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MirrorPost AI - Diagnostic Tool"""

import sys
import os
import subprocess

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def check_python():
    print("\n[Check 1] Python Environment")
    print(f"  Version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    return True

def check_env_file():
    print("\n[Check 2] .env File")
    if os.path.exists(".env"):
        print("  [OK] .env file exists")
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if "GOOGLE_API_KEY" in content:
                print("  [OK] GOOGLE_API_KEY is configured")
                # Don't print the actual key
                print(f"  Content: GOOGLE_API_KEY=***{content.split('=')[1][-10:]}")
            else:
                print("  [ERROR] GOOGLE_API_KEY not found in .env")
                return False
        return True
    else:
        print("  [ERROR] .env file NOT found!")
        print("  Please create .env file with:")
        print("  GOOGLE_API_KEY=your_actual_key")
        return False

def check_files():
    print("\n[Check 3] Core Files")
    files = [
        "backend.py",
        "server.py",
        "SaaS.html",
        "Landing page.html",
        "start_backend.bat",
        "start_frontend.bat"
    ]
    all_exist = True
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  [OK] {file} ({size} bytes)")
        else:
            print(f"  [ERROR] {file} is missing!")
            all_exist = False
    return all_exist

def check_dependencies():
    print("\n[Check 4] Python Dependencies")
    deps = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "dotenv",
        ("google.genai", "google-genai"),
        ("PIL", "Pillow")
    ]

    all_installed = True
    for dep in deps:
        if isinstance(dep, tuple):
            import_name, package_name = dep
        else:
            import_name = package_name = dep

        try:
            __import__(import_name)
            print(f"  [OK] {package_name} is installed")
        except ImportError:
            print(f"  [ERROR] {package_name} is NOT installed!")
            all_installed = False

    return all_installed

def check_ports():
    print("\n[Check 5] Port Status")
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            encoding='gbk'  # Windows uses GBK encoding
        )
        output = result.stdout

        # Check port 8000
        if ":8000" in output:
            print("  [WARNING] Port 8000 is occupied")
            for line in output.split('\n'):
                if ":8000" in line:
                    print(f"    {line.strip()}")
        else:
            print("  [OK] Port 8000 is free")

        # Check port 8080
        if ":8080" in output:
            print("  [WARNING] Port 8080 is occupied")
            for line in output.split('\n'):
                if ":8080" in line:
                    print(f"    {line.strip()}")
        else:
            print("  [OK] Port 8080 is free")
    except Exception as e:
        print(f"  [WARNING] Could not check ports: {e}")

def main():
    print_header("MirrorPost AI - Diagnostic Tool")
    print(f"\nCurrent Directory: {os.getcwd()}\n")

    checks = {
        "Python": check_python(),
        ".env File": check_env_file(),
        "Core Files": check_files(),
        "Dependencies": check_dependencies(),
    }

    check_ports()

    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in checks.items():
        status = "[OK]" if passed else "[FAIL]"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("\n  All checks passed! You can start the project.")
        print("\n  Next step:")
        print("  1. Double click: start.bat")
        print("  2. Or run: python server.py")
    else:
        print("\n  Some checks failed. Please fix the errors above.")
        print("\n  Common fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Create .env file with GOOGLE_API_KEY=your_key")

    print("\n")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

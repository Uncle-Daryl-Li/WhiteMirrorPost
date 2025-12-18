#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import ast

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        code = f.read()

    ast.parse(code)
    print("OK: app.py syntax is valid")

    checks = [
        ("with st.sidebar:", "Sidebar definition"),
        ("Control Panel", "Control Panel title"),
        ("Generation Settings", "Generation Settings"),
        ("Style Library", "Style Library"),
        ("Assets", "Assets section"),
        ("Advanced", "Advanced section")
    ]

    for pattern, name in checks:
        if pattern in code:
            print(f"OK: Found {name}")
        else:
            print(f"ERROR: Missing {name}")

    print("\nCheck complete!")

except SyntaxError as e:
    print(f"ERROR: Syntax error at line {e.lineno}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

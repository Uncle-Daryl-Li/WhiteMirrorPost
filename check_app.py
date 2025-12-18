#!/usr/bin/env python
# 检查 app.py 是否有语法错误

import sys
import ast

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        code = f.read()

    # 尝试解析代码
    ast.parse(code)
    print("✅ app.py 语法检查通过！")
    print("📋 代码结构检查...")

    # 检查关键部分
    if "with st.sidebar:" in code:
        print("✅ 找到侧边栏定义")
    else:
        print("❌ 未找到侧边栏定义")

    if "st.title(\"🎛️ Control Panel\")" in code:
        print("✅ 找到控制台标题")
    else:
        print("❌ 未找到控制台标题")

    if "st.expander(\"📂 生成设置" in code:
        print("✅ 找到生成设置区")
    else:
        print("❌ 未找到生成设置区")

    if "st.expander(\"🎨 风格库" in code:
        print("✅ 找到风格库区")
    else:
        print("❌ 未找到风格库区")

    if "st.expander(\"🧩 素材管理" in code:
        print("✅ 找到素材管理区")
    else:
        print("❌ 未找到素材管理区")

    if "st.expander(\"⚙️ 高级配置" in code:
        print("✅ 找到高级配置区")
    else:
        print("❌ 未找到高级配置区")

    print("\n✨ 检查完成！app.py 应该可以正常运行。")

except SyntaxError as e:
    print(f"❌ 语法错误：{e}")
    print(f"   位置：第 {e.lineno} 行")
    sys.exit(1)
except Exception as e:
    print(f"❌ 检查失败：{e}")
    sys.exit(1)

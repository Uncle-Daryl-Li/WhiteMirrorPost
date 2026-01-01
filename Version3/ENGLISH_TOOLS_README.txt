╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         IMPORTANT: Use English Version Tools                  ║
║         (Chinese version has encoding issues)                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════
  Problem: Chinese Characters Show Garbled Text
═══════════════════════════════════════════════════════════════

The original .bat files with Chinese characters have encoding
issues on your system. Please use the ENGLISH version tools below.


═══════════════════════════════════════════════════════════════
  SOLUTION: Use These English Tools
═══════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────────────────┐
│  Step 1: Run Diagnostic (Python Version - RECOMMENDED)       │
└───────────────────────────────────────────────────────────────┘

Double click:
  ► diagnose.py

This will check:
  • Python environment
  • .env file configuration
  • Core files existence
  • Python dependencies
  • Port availability

Copy ALL the output and tell me the results!


┌───────────────────────────────────────────────────────────────┐
│  Step 2: Run Diagnostic (Batch Version - Alternative)        │
└───────────────────────────────────────────────────────────────┘

If diagnose.py doesn't work, try:
  ► diagnose.bat

This is a simpler version using only English characters.


┌───────────────────────────────────────────────────────────────┐
│  Step 3: Start the Project (After Diagnostic Passes)         │
└───────────────────────────────────────────────────────────────┘

Double click:
  ► start.bat

This will:
  • Check Python and .env
  • Start Backend server
  • Start Frontend server
  • Open browser automatically


═══════════════════════════════════════════════════════════════
  Quick Command Line Alternative
═══════════════════════════════════════════════════════════════

If the .bat files still don't work, use Command Prompt:

1. Open CMD in Version3 folder:
   - Hold Shift + Right Click in folder
   - Select "Open command window here" or "Open PowerShell window here"

2. Run diagnostic:
   python diagnose.py

3. If all checks pass, start manually:
   Terminal 1: python server.py
   Terminal 2: python -m http.server 8080

4. Open browser:
   http://localhost:8080/Landing page.html


═══════════════════════════════════════════════════════════════
  File List (English Tools)
═══════════════════════════════════════════════════════════════

✓ diagnose.py           - Python diagnostic script (BEST)
✓ diagnose.bat          - Batch diagnostic script
✓ start.bat             - Quick start script
✓ ENGLISH_TOOLS_README.txt - This file


Old files (Don't use if you see garbled text):
✗ 诊断问题.bat
✗ 一键启动.bat
✗ 手动启动_调试版.bat


═══════════════════════════════════════════════════════════════
  What to Do Next
═══════════════════════════════════════════════════════════════

1. Double click: diagnose.py
2. Copy ALL the output text
3. Tell me what you see
4. I will help you fix any errors


═══════════════════════════════════════════════════════════════

         Please run: diagnose.py

         Then copy the results and show me!

═══════════════════════════════════════════════════════════════

# MirrorPost AI - 快速启动教程

<div align="center">

**AI驱动的智能海报生成工具 第三版**

基于 HTML + FastAPI + Google Gemini API

</div>

---

## 📖 目录

- [项目简介](#项目简介)
- [快速开始（3步启动）](#快速开始3步启动)
- [详细安装步骤](#详细安装步骤)
- [常见问题](#常见问题)
- [项目结构](#项目结构)
- [API文档](#api文档)

---

## 项目简介

MirrorPost AI 第三版是一个现代化的AI海报生成工具，具有：

- 🎨 **精美UI界面** - 极光动画、霓虹光效、流畅交互
- 🤖 **AI智能生成** - 基于Google Gemini 3 Pro图像生成模型
- ⚙️ **丰富配置** - 多种纵横比、风格预设、Thinking模式
- 🖼️ **批量生成** - 一次最多生成10张不同风格的海报

**技术栈**:
- 前端：HTML5 + CSS3 + Vanilla JavaScript
- 后端：Python FastAPI
- AI：Google Gemini API

---

## 快速开始（3步启动）

### ⚡ 步骤1：检查环境

确保已安装：
```bash
# 检查Python版本（需要 3.8+）
python --version

# 应显示：Python 3.8.0 或更高
```

### ⚡ 步骤2：配置API Key

1. 获取Google API Key：
   - 访问：https://aistudio.google.com/app/apikey
   - 登录Google账号
   - 点击"Create API Key"
   - 复制生成的密钥

2. 配置到 `.env` 文件：
   ```bash
   # 打开或创建 .env 文件
   notepad .env

   # 写入以下内容（替换为你的实际Key）
   GOOGLE_API_KEY=你的实际API_Key
   ```

### ⚡ 步骤3：启动项目

**Windows用户（推荐）**:
```bash
# 方式1：双击批处理文件
start_backend.bat  # 启动后端
start_frontend.bat # 启动前端

# 方式2：命令行启动
cd D:\WhiteMirror\Post
python server.py           # 窗口1：后端
python -m http.server 8080 # 窗口2：前端
```

**访问应用**:
```
打开浏览器，访问：
http://localhost:8080/Landing page.html
```

---

## 详细安装步骤

### 1️⃣ 安装依赖

```bash
# 进入项目目录
cd D:\WhiteMirror\Post

# 安装Python依赖
pip install -r requirements.txt
```

**dependencies.txt 包含**:
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.0.0
python-dotenv>=1.0.0
google-genai>=0.3.0
Pillow>=10.0.0
```

---

### 2️⃣ 启动后端服务器

#### 方法A：使用批处理脚本（推荐）

```bash
# 直接双击文件
start_backend.bat

# 或在CMD中运行
cd D:\WhiteMirror\Post
start_backend.bat
```

**预期输出**:
```
========================================
  MirrorPost AI - Backend Server
========================================

Starting FastAPI server...
API: http://localhost:8000
Docs: http://localhost:8000/docs

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 方法B：直接使用Python

```bash
cd D:\WhiteMirror\Post
python server.py
```

#### 验证后端启动成功

打开浏览器，访问：
```
http://localhost:8000
```

应显示：
```json
{
  "service": "MirrorPost AI API",
  "status": "running",
  "version": "2.0"
}
```

查看完整API文档：
```
http://localhost:8000/docs
```

---

### 3️⃣ 启动前端服务器

> ⚠️ **重要**: 必须使用HTTP服务器，不能直接双击HTML文件打开！

#### 方法A：使用Python HTTP服务器（推荐）

```bash
# 新开一个CMD窗口
cd D:\WhiteMirror\Post
python -m http.server 8080
```

**预期输出**:
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

**访问应用**:
```
http://localhost:8080/Landing page.html
```

#### 方法B：使用批处理脚本

```bash
# 双击文件
start_frontend.bat

# 或在CMD中
cd D:\WhiteMirror\Post
start_frontend.bat
```

#### 方法C：使用VS Code Live Server

1. 在VS Code中安装 "Live Server" 扩展
2. 右键点击 `Landing page.html`
3. 选择 "Open with Live Server"

**注意**: 如果使用Live Server，需要修改后端CORS配置：

```python
# 编辑 server.py，第20行
allow_origins=[
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:5500",  # 添加Live Server地址
],
```

然后重启后端服务器。

---

### 4️⃣ 开始使用

#### 登录页面 (Landing page.html)

1. 打开 `http://localhost:8080/Landing page.html`
2. 点击"实现创想"按钮
3. 自动跳转到工作区

#### 工作区页面 (SaaS.html)

**左侧边栏配置**:

1. **生成设置**:
   - 海报比例：9:16 / 16:9 / 1:1 / 3:4 / 4:3
   - 生成数量：1-10张

2. **风格库**:
   - 自动匹配 (Auto)
   - 极简主义 (Minimalist)
   - 商务科技 (Tech)
   - 温暖手绘 (Hand-drawn)
   - 风格强度：0.00-1.00

**生成海报**:

1. 在中央输入框输入描述，例如：
   ```
   赛博朋克风格的城市夜景，霓虹灯光，未来感建筑，高清壁纸
   ```

2. 点击右下角生成按钮（上箭头图标）

3. 观看动画效果：
   - 极光收缩
   - 霓虹旋转
   - API调用

4. 查看生成结果

**切换模式**:

- 点击"脑"图标 = Thinking模式（更深入思考，质量更高，速度较慢）
- 点击"闪电"图标 = Fast模式（快速生成）

---

## 常见问题

### ❓ Q1: 提示"Failed to fetch"错误？

**原因**: 后端服务器未启动或CORS配置问题

**解决方案**:
1. 确认后端正在运行：访问 `http://localhost:8000`
2. 检查是否通过HTTP服务器打开前端（URL应是 `http://` 开头）
3. 检查控制台（F12）查看具体错误信息

---

### ❓ Q2: 点击生成后无反应？

**检查清单**:
- [ ] 后端服务器正在运行（`python server.py`）
- [ ] 前端通过HTTP服务器访问（不是直接打开文件）
- [ ] 打开浏览器控制台（F12）检查错误
- [ ] 输入框有内容

---

### ❓ Q3: 显示"GOOGLE_API_KEY 未在 .env 文件中设置"？

**解决方案**:
1. 检查项目根目录是否有 `.env` 文件
2. 打开 `.env` 文件，确认格式：
   ```
   GOOGLE_API_KEY=你的实际Key
   ```
3. 确保没有多余的空格或引号
4. 重启后端服务器

---

### ❓ Q4: API返回403 PERMISSION_DENIED错误？

**原因**: API Key无效或已泄露被禁用

**解决方案**:
1. 前往 https://aistudio.google.com/app/apikey
2. 生成新的API Key
3. 更新 `.env` 文件
4. 重启后端服务器

---

### ❓ Q5: 生成速度很慢？

**优化建议**:
- 减少生成数量（设置为1-2张）
- 切换到Fast模式（闪电图标）
- 检查网络连接

**参考时间**:
- Fast模式：约10-20秒/张
- Thinking模式：约30-60秒/张

---

### ❓ Q6: 无法打开HTML文件（双击无效）？

**原因**: 浏览器CORS安全策略阻止 `file://` 协议访问API

**解决方案**: 必须使用HTTP服务器，参考"启动前端服务器"章节

---

### ❓ Q7: 端口8000被占用？

**检查占用**:
```bash
# Windows
netstat -ano | findstr :8000

# 查看PID，然后结束进程
taskkill /PID <进程ID> /F
```

**或修改端口**:
编辑 `server.py` 最后一行：
```python
uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
```

同时修改前端 `SaaS.html` 第464行：
```javascript
const response = await fetch('http://localhost:8001/api/generate', {
```

---

## 项目结构

```
D:\WhiteMirror\Post\
│
├── 📄 Landing page.html          # 登录/首页
├── 📄 SaaS.html                  # 主工作区界面
├── 📄 app.py                     # Streamlit版本（旧版）
│
├── 🐍 backend.py                 # 核心生成逻辑
├── 🐍 server.py                  # FastAPI服务器
├── 🐍 test_connection.py         # 连接测试脚本
│
├── ⚙️ .env                       # 环境变量配置
├── 📋 requirements.txt           # Python依赖
│
├── 🪟 start_backend.bat          # 后端启动脚本
├── 🪟 start_frontend.bat         # 前端启动脚本
│
├── 📖 README.md                  # 本文件
├── 📖 README_API.md              # API数据流文档
├── 📖 frontend-backend_problem.md # 前后端对接问题文档
│
├── 🖼️ logo.png                   # 项目Logo
│
└── 📁 generated_posters/         # 生成的海报保存目录
    └── poster_20251230_*.png
```

---

## API文档

### 端点1: 健康检查

**请求**:
```http
GET http://localhost:8000/
```

**响应**:
```json
{
  "service": "MirrorPost AI API",
  "status": "running",
  "version": "2.0"
}
```

---

### 端点2: 生成海报

**请求**:
```http
POST http://localhost:8000/api/generate
Content-Type: application/json

{
  "prompt": "赛博朋克风格的城市夜景",
  "aspect_ratio": "9:16",
  "count": 4,
  "preset_style": "Tech",
  "style_intensity": 0.8,
  "negative_prompt": "低质量，模糊",
  "thinking_mode": true
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| `prompt` | string | ✅ | 海报描述 | 任意文字 |
| `aspect_ratio` | string | ❌ | 纵横比 | "9:16", "16:9", "1:1", "3:4", "4:3" |
| `count` | integer | ❌ | 生成数量 | 1-10 |
| `preset_style` | string | ❌ | 预设风格 | "Auto", "Minimalist", "Tech", "Hand-drawn" |
| `style_intensity` | float | ❌ | 风格强度 | 0.0-1.0 |
| `negative_prompt` | string | ❌ | 负面提示词 | 任意文字 |
| `thinking_mode` | boolean | ❌ | 思考模式 | true/false |

**响应**:
```json
{
  "success": true,
  "images": [
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  ],
  "message": "成功生成 4 张海报"
}
```

**错误响应**:
```json
{
  "detail": "GOOGLE_API_KEY 未在 .env 文件中设置"
}
```

---

### 使用curl测试API

```bash
# 健康检查
curl http://localhost:8000/

# 生成海报
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "测试海报",
    "aspect_ratio": "9:16",
    "count": 1,
    "preset_style": "Auto",
    "style_intensity": 0.5,
    "thinking_mode": false
  }'
```

---

## 高级配置

### 修改CORS允许的域名

编辑 `server.py`，第18-24行：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite
        "http://localhost:8080",      # Python HTTP Server
        "http://127.0.0.1:5500",      # VS Code Live Server
        "http://your-domain.com",     # 添加你的域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 修改生成参数默认值

编辑 `SaaS.html`，找到对应的HTML元素修改默认值：

```html
<!-- 默认生成数量 -->
<input type="range" min="1" max="10" value="4" ... />

<!-- 默认风格强度 -->
<input type="range" min="0" max="1" step="0.01" value="0.65" ... />
```

---

## 开发建议

### 调试模式

**后端调试**:
```python
# server.py 最后一行修改为：
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug", reload=True)
```

**前端调试**:
- 打开浏览器开发者工具（F12）
- 查看 Console 标签页的日志
- 查看 Network 标签页的请求

### 查看后端日志

后端会自动打印生成日志：
```
[API] 收到生成请求:
  - 提示词: 赛博朋克风格的城市夜景
  - 比例: 9:16
  - 数量: 4
  - 风格: Tech
  - Thinking 模式: True

正在生成第 1/4 张海报...
已保存: generated_posters/poster_20251230_143022_1.png
正在生成第 2/4 张海报...
...
```

---

## 完整启动流程总结

```bash
# ============= 终端窗口1: 后端 =============
cd D:\WhiteMirror\Post
python server.py

# 等待输出：Uvicorn running on http://0.0.0.0:8000

# ============= 终端窗口2: 前端 =============
cd D:\WhiteMirror\Post
python -m http.server 8080

# 等待输出：Serving HTTP on :: port 8080

# ============= 浏览器 =============
# 访问：http://localhost:8080/Landing page.html
```

---

## 卸载/清理

```bash
# 删除生成的海报
rmdir /S /Q generated_posters

# 删除Python缓存
rmdir /S /Q __pycache__

# 卸载依赖（可选）
pip uninstall -r requirements.txt -y
```

---

## 更新日志

### v3.0 (2025-12-30)
- ✨ 全新HTML前端界面（极光+霓虹效果）
- 🔌 前后端完全分离架构
- 🚀 FastAPI后端服务器
- 📱 响应式设计
- 🎨 多种风格预设

### v2.0 (之前)
- React + TypeScript前端
- FastAPI后端

### v1.0 (最初)
- Streamlit一体化应用

---

## 许可证

本项目仅供学习和研究使用。

---

## 联系方式

如有问题，请查阅：
- `frontend-backend_problem.md` - 详细问题解决文档
- `README_API.md` - 完整API数据流文档
- GitHub Issues（如果有仓库）

---

<div align="center">

**Happy Creating! 🎨**

Made with ❤️ by WhiteMirror Team

</div>

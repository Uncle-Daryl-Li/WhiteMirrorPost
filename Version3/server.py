# FastAPI 服务器 - 连接前后端
# 此文件提供 RESTful API 接口供前端调用

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import base64
from io import BytesIO
from PIL import Image
import json
import os
from datetime import datetime

from backend import generate_posters

# 创建 FastAPI 应用
app = FastAPI(title="MirrorPost AI API", version="2.0")

# 配置 CORS - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:8080"],  # 允许前端端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求数据模型
class GenerateRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "9:16"
    count: int = 1
    preset_style: str = "Auto"
    style_intensity: float = 0.5
    negative_prompt: Optional[str] = None
    thinking_mode: bool = True
    reference_image: Optional[str] = None  # Base64 编码的参考图片（用于图生图）
    logo_image: Optional[str] = None  # Base64 编码的 Logo 图片
    qrcode_image: Optional[str] = None  # Base64 编码的二维码图片
    combo_images: Optional[List[str]] = None  # Base64 编码的品牌组合图片列表


# 响应数据模型
class GenerateResponse(BaseModel):
    success: bool
    images: List[str]  # Base64 编码的图片列表
    message: str
    error_reason: Optional[str] = None  # 错误原因（部分成功时）


# 历史对话数据模型
class Turn(BaseModel):
    prompt: str
    images: List[str]  # Base64 编码的图片


class Session(BaseModel):
    id: str
    title: str
    timestamp: str
    turns: List[Turn]


class SessionCreate(BaseModel):
    id: str
    title: str
    timestamp: str


class SessionsResponse(BaseModel):
    success: bool
    sessions: List[Session]


def image_to_base64(image: Image.Image) -> str:
    """将 PIL Image 转换为 Base64 字符串"""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


def base64_to_image(base64_str: str) -> Image.Image:
    """将 Base64 字符串转换为 PIL Image"""
    # 移除 data:image/png;base64, 前缀（如果存在）
    if ',' in base64_str:
        base64_str = base64_str.split(',', 1)[1]

    # 解码 Base64
    img_bytes = base64.b64decode(base64_str)
    image = Image.open(BytesIO(img_bytes))
    return image


# 历史对话存储管理
SESSIONS_DIR = "sessions_data"

def ensure_sessions_dir():
    """确保存储目录存在"""
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)

def get_sessions_file():
    """获取会话列表文件路径"""
    ensure_sessions_dir()
    return os.path.join(SESSIONS_DIR, "sessions.json")

def load_sessions() -> List[dict]:
    """从文件加载所有会话"""
    sessions_file = get_sessions_file()
    if not os.path.exists(sessions_file):
        return []
    try:
        with open(sessions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载会话失败: {str(e)}")
        return []

def save_sessions(sessions: List[dict]):
    """保存所有会话到文件"""
    sessions_file = get_sessions_file()
    try:
        with open(sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存会话失败: {str(e)}")
        raise


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "service": "MirrorPost AI API",
        "status": "running",
        "version": "2.0"
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    生成海报 API

    接收前端参数，调用后端生成逻辑，返回 Base64 图片
    """
    try:
        # 构建风格提示词
        style_prompt = None
        if request.preset_style != "Auto":
            style_keywords = {
                "Minimalist": "minimalist design, clean layout, simple geometric shapes, plenty of white space",
                "Tech": "tech-inspired design, modern digital aesthetic, futuristic elements",
                "Hand-drawn": "hand-drawn illustration style, warm colors, artistic and friendly"
            }
            style_keyword = style_keywords.get(request.preset_style, "")
            if style_keyword:
                style_prompt = f"{style_keyword}. Style strength: {request.style_intensity}"

        # 合并提示词
        final_prompt = request.prompt
        if style_prompt:
            final_prompt = f"{request.prompt}. Style: {style_prompt}"
        if request.negative_prompt:
            final_prompt = f"{final_prompt}. Avoid: {request.negative_prompt}"

        # 处理参考图片（图生图）
        reference_img = None
        if request.reference_image:
            try:
                reference_img = base64_to_image(request.reference_image)
                print(f"  - 参考图片: 已接收 ({reference_img.size})")
            except Exception as e:
                print(f"  - 参考图片解码失败: {str(e)}")

        # 处理 Logo 图片
        logo_img = None
        if request.logo_image:
            try:
                logo_img = base64_to_image(request.logo_image)
                print(f"  - Logo 图片: 已接收 ({logo_img.size})")
            except Exception as e:
                print(f"  - Logo 图片解码失败: {str(e)}")

        # 处理二维码图片
        qrcode_img = None
        if request.qrcode_image:
            try:
                qrcode_img = base64_to_image(request.qrcode_image)
                print(f"  - 二维码图片: 已接收 ({qrcode_img.size})")
            except Exception as e:
                print(f"  - 二维码图片解码失败: {str(e)}")

        # 处理品牌组合图片
        combo_imgs = None
        if request.combo_images:
            try:
                combo_imgs = []
                for i, img_b64 in enumerate(request.combo_images):
                    img = base64_to_image(img_b64)
                    combo_imgs.append(img)
                print(f"  - 品牌组合图片: 已接收 {len(combo_imgs)} 张")
            except Exception as e:
                print(f"  - 品牌组合图片解码失败: {str(e)}")
                combo_imgs = None

        print(f"\n[API] 收到生成请求:")
        print(f"  - 提示词: {request.prompt}")
        print(f"  - 比例: {request.aspect_ratio}")
        print(f"  - 数量: {request.count}")
        print(f"  - 风格: {request.preset_style}")
        print(f"  - Thinking 模式: {request.thinking_mode}")
        print(f"  - 图生图模式: {'是' if reference_img else '否'}")
        print(f"  - Logo: {'是' if logo_img else '否'}")
        print(f"  - 二维码: {'是' if qrcode_img else '否'}")
        print(f"  - 品牌组合: {'是 (' + str(len(combo_imgs)) + ' 张)' if combo_imgs else '否'}")
        print(f"  - 最终提示词: {final_prompt[:100]}...")

        # 调用后端生成
        generated_images, error_reason = generate_posters(
            user_prompt=final_prompt,
            aspect_ratio=request.aspect_ratio,
            num_images=request.count,
            thinking_mode=request.thinking_mode,
            reference_image=reference_img,
            logo_image=logo_img,
            qrcode_image=qrcode_img,
            combo_images=combo_imgs
        )

        # 转换为 Base64
        base64_images = []
        for img in generated_images:
            base64_str = image_to_base64(img)
            base64_images.append(base64_str)

        print(f"[API] 成功生成 {len(base64_images)} 张海报")
        if error_reason:
            print(f"[API] 部分失败原因: {error_reason}")

        return GenerateResponse(
            success=True,
            images=base64_images,
            message=f"成功生成 {len(base64_images)} 张海报",
            error_reason=error_reason
        )

    except ValueError as e:
        # 配置错误（如缺少 API Key）
        print(f"[API] 配置错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # 其他错误
        print(f"[API] 生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


# ============= 历史对话 API =============

@app.post("/api/sessions")
async def create_or_update_session(session: Session):
    """创建或更新会话"""
    try:
        sessions = load_sessions()

        # 查找是否已存在
        existing_index = None
        for i, s in enumerate(sessions):
            if s['id'] == session.id:
                existing_index = i
                break

        # 转换为字典
        session_dict = session.model_dump()

        if existing_index is not None:
            # 更新已有会话
            sessions[existing_index] = session_dict
            print(f"[API] 更新会话: {session.id}")
        else:
            # 新建会话（插入到开头）
            sessions.insert(0, session_dict)
            print(f"[API] 创建会话: {session.id}")

        save_sessions(sessions)

        return {
            "success": True,
            "message": "会话保存成功",
            "session_id": session.id
        }
    except Exception as e:
        print(f"[API] 保存会话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"保存会话失败: {str(e)}")


@app.get("/api/sessions")
async def get_all_sessions():
    """获取所有会话列表"""
    try:
        sessions = load_sessions()
        print(f"[API] 获取会话列表: {len(sessions)} 个会话")
        return {
            "success": True,
            "sessions": sessions
        }
    except Exception as e:
        print(f"[API] 获取会话列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取会话列表失败: {str(e)}")


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """获取特定会话详情"""
    try:
        sessions = load_sessions()

        # 查找会话
        for session in sessions:
            if session['id'] == session_id:
                print(f"[API] 获取会话详情: {session_id}")
                return {
                    "success": True,
                    "session": session
                }

        raise HTTPException(status_code=404, detail="会话不存在")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] 获取会话详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取会话详情失败: {str(e)}")


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    try:
        sessions = load_sessions()

        # 查找并删除
        initial_length = len(sessions)
        sessions = [s for s in sessions if s['id'] != session_id]

        if len(sessions) == initial_length:
            raise HTTPException(status_code=404, detail="会话不存在")

        save_sessions(sessions)
        print(f"[API] 删除会话: {session_id}")

        return {
            "success": True,
            "message": "会话删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] 删除会话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除会话失败: {str(e)}")


@app.post("/api/sessions/{session_id}/turns")
async def add_turn_to_session(session_id: str, turn: Turn):
    """向会话添加新的对话轮次"""
    try:
        sessions = load_sessions()

        # 查找会话
        for session in sessions:
            if session['id'] == session_id:
                # 添加新的轮次
                if 'turns' not in session:
                    session['turns'] = []
                session['turns'].append(turn.model_dump())

                save_sessions(sessions)
                print(f"[API] 向会话 {session_id} 添加新轮次")

                return {
                    "success": True,
                    "message": "轮次添加成功"
                }

        raise HTTPException(status_code=404, detail="会话不存在")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] 添加轮次失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"添加轮次失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  MirrorPost AI API Server")
    print("=" * 50)
    print("API Address: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

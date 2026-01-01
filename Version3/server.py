# FastAPI 服务器 - 连接前后端
# 此文件提供 RESTful API 接口供前端调用

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import base64
from io import BytesIO
from PIL import Image

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


# 响应数据模型
class GenerateResponse(BaseModel):
    success: bool
    images: List[str]  # Base64 编码的图片列表
    message: str


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

        print(f"\n[API] 收到生成请求:")
        print(f"  - 提示词: {request.prompt}")
        print(f"  - 比例: {request.aspect_ratio}")
        print(f"  - 数量: {request.count}")
        print(f"  - 风格: {request.preset_style}")
        print(f"  - Thinking 模式: {request.thinking_mode}")
        print(f"  - 图生图模式: {'是' if reference_img else '否'}")
        print(f"  - 最终提示词: {final_prompt[:100]}...")

        # 调用后端生成
        generated_images = generate_posters(
            user_prompt=final_prompt,
            aspect_ratio=request.aspect_ratio,
            num_images=request.count,
            thinking_mode=request.thinking_mode,
            reference_image=reference_img  # 传递参考图片
        )

        # 转换为 Base64
        base64_images = []
        for img in generated_images:
            base64_str = image_to_base64(img)
            base64_images.append(base64_str)

        print(f"[API] 成功生成 {len(base64_images)} 张海报")

        return GenerateResponse(
            success=True,
            images=base64_images,
            message=f"成功生成 {len(base64_images)} 张海报"
        )

    except ValueError as e:
        # 配置错误（如缺少 API Key）
        print(f"[API] 配置错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # 其他错误
        print(f"[API] 生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  MirrorPost AI API Server")
    print("=" * 50)
    print("API Address: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

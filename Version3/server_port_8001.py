# FastAPI Server - Using Port 8001
# This is a copy of server.py with modified port

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import base64
from io import BytesIO
from PIL import Image

from backend import generate_posters

# Create FastAPI app
app = FastAPI(title="MirrorPost AI API", version="2.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class GenerateRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "9:16"
    count: int = 1
    preset_style: str = "Auto"
    style_intensity: float = 0.5
    negative_prompt: Optional[str] = None
    thinking_mode: bool = True


# Response model
class GenerateResponse(BaseModel):
    success: bool
    images: List[str]
    message: str


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to Base64 string"""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "service": "MirrorPost AI API",
        "status": "running",
        "version": "2.0",
        "port": "8001"
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Generate poster API"""
    try:
        # Build style prompt
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

        # Merge prompts
        final_prompt = request.prompt
        if style_prompt:
            final_prompt = f"{request.prompt}. Style: {style_prompt}"
        if request.negative_prompt:
            final_prompt = f"{final_prompt}. Avoid: {request.negative_prompt}"

        print(f"\n[API - Port 8001] Generate request received:")
        print(f"  - Prompt: {request.prompt}")
        print(f"  - Aspect ratio: {request.aspect_ratio}")
        print(f"  - Count: {request.count}")
        print(f"  - Style: {request.preset_style}")
        print(f"  - Thinking mode: {request.thinking_mode}")
        print(f"  - Final prompt: {final_prompt[:100]}...")

        # Call backend
        generated_images = generate_posters(
            user_prompt=final_prompt,
            aspect_ratio=request.aspect_ratio,
            num_images=request.count,
            thinking_mode=request.thinking_mode
        )

        # Convert to Base64
        base64_images = []
        for img in generated_images:
            base64_str = image_to_base64(img)
            base64_images.append(base64_str)

        print(f"[API - Port 8001] Successfully generated {len(base64_images)} posters")

        return GenerateResponse(
            success=True,
            images=base64_images,
            message=f"Successfully generated {len(base64_images)} posters"
        )

    except ValueError as e:
        print(f"[API - Port 8001] Configuration error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print(f"[API - Port 8001] Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  MirrorPost AI API Server - Port 8001")
    print("=" * 50)
    print("API Address: http://localhost:8001")
    print("API Docs: http://localhost:8001/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")

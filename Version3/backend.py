# MirrorPost AI - 后端逻辑
# 此文件用于处理核心业务逻辑

import os
from datetime import datetime
from io import BytesIO
from typing import List, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# 加载环境变量
load_dotenv()


def generate_posters(
    user_prompt: str,
    aspect_ratio: str = "9:16",
    num_images: int = 8,
    thinking_mode: bool = True,
    reference_image: Optional[Image.Image] = None,
    style_prompt: Optional[str] = None,
    logo_image: Optional[Image.Image] = None,
    qrcode_image: Optional[Image.Image] = None,
    slogan: Optional[str] = None
) -> List[Image.Image]:
    """
    批量生成海报，支持多种模式

    参数:
        user_prompt (str): 用户输入的海报描述
        aspect_ratio (str): 海报纵横比，默认 "9:16"
        num_images (int): 生成数量，默认 8 张
        thinking_mode (bool): 是否启用 Thinking 模式，默认 True
        reference_image (Image.Image): 参考图片（图生图功能）
        style_prompt (str): 风格描述（从风格库加载）
        logo_image (Image.Image): Logo 图片
        qrcode_image (Image.Image): 二维码图片
        slogan (str): Slogan 文案

    返回:
        List[Image.Image]: 生成的海报列表
    """
    # 初始化客户端
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY 未在 .env 文件中设置")

    client = genai.Client(api_key=api_key)

    # 构建提示词
    enhanced_prompt = _build_prompt(
        user_prompt, thinking_mode, style_prompt, reference_image,
        logo_image, qrcode_image, slogan
    )

    # 配置模型参数
    config = types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size="2k"
        )
    )

    # 批量生成
    generated_images = []
    for i in range(num_images):
        print(f"正在生成第 {i+1}/{num_images} 张海报...")

        try:
            # 准备内容（包含提示词和所有图片素材）
            contents = [enhanced_prompt]

            # 添加参考图片
            if reference_image:
                contents.append(reference_image)

            # 添加 Logo
            if logo_image:
                contents.append(logo_image)

            # 添加二维码
            if qrcode_image:
                contents.append(qrcode_image)

            # 如果只有文本，不用列表
            if len(contents) == 1:
                contents = contents[0]

            # 生成内容
            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=contents,
                config=config
            )

            # 提取图片
            image = _extract_image_from_response(response)
            if image:
                generated_images.append(image)
                # 保存到本地
                _save_image(image, i)
            else:
                print(f"警告: 第 {i+1} 张海报生成失败，跳过")

        except Exception as e:
            print(f"生成第 {i+1} 张时出错: {str(e)}")
            continue

    if not generated_images:
        raise ValueError("所有海报生成均失败")

    print(f"成功生成 {len(generated_images)} 张海报")
    return generated_images


def _build_prompt(
    user_prompt: str,
    thinking_mode: bool,
    style_prompt: Optional[str],
    reference_image: Optional[Image.Image],
    logo_image: Optional[Image.Image],
    qrcode_image: Optional[Image.Image],
    slogan: Optional[str]
) -> str:
    """构建完整的提示词"""
    prompt_parts = []

    # Thinking 模式前缀
    if thinking_mode:
        prompt_parts.append(
            "First, analyze the design requirements and plan the visual strategy. "
            "Then generate the poster based on your analysis."
        )

    # 用户输入
    prompt_parts.append(user_prompt)

    # 风格描述
    if style_prompt:
        prompt_parts.append(f"Style reference: {style_prompt}")

    # 图生图说明
    if reference_image:
        prompt_parts.append(
            "Use the provided reference image as inspiration for style, "
            "composition, or color palette."
        )

    # 素材要求
    asset_requirements = []
    if logo_image:
        asset_requirements.append("include a logo in appropriate position")
    if qrcode_image:
        asset_requirements.append("include a QR code (typically bottom corner)")
    if slogan:
        asset_requirements.append(f"include slogan text: '{slogan}'")

    if asset_requirements:
        prompt_parts.append("Asset requirements: " + ", ".join(asset_requirements))

    # 基础要求
    prompt_parts.append("high quality poster design, professional typography")

    return ". ".join(prompt_parts)


def _extract_image_from_response(response) -> Optional[Image.Image]:
    """从响应中提取图片"""
    for part in response.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            try:
                image_bytes = part.inline_data.data
                return Image.open(BytesIO(image_bytes))
            except Exception as e:
                print(f"图片解析失败: {str(e)}")
                continue
    return None


def _save_image(image: Image.Image, index: int):
    """保存图片到本地"""
    # 创建输出目录
    output_dir = "generated_posters"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"poster_{timestamp}_{index+1}.png")
    image.save(output_path)
    print(f"已保存: {output_path}")

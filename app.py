# MirrorPost AI - 前端界面
# 此文件使用 Streamlit 构建用户界面

import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from backend import generate_posters
from style_manager import StyleManager
from asset_manager import AssetManager

# 加载环境变量
load_dotenv()

# 初始化管理器
style_manager = StyleManager()
asset_manager = AssetManager()

# 页面配置
st.set_page_config(
    page_title="MirrorPost AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"  # 默认展开控制台
)

# Google Gemini 风格主题 CSS
st.markdown("""
<style>
    /* 主色调：白色背景 */
    .stApp {
        background-color: #ffffff;
        color: #202124;
    }

    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} 不隐藏header，保留侧边栏控制按钮 */

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }

    /* 侧边栏展开/收起按钮样式 */
    [data-testid="collapsedControl"] {
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        z-index: 999999 !important;
        background-color: #f8f9fa !important;
        padding: 0.5rem !important;
        border-right: 1px solid #e0e0e0 !important;
        border-bottom: 1px solid #e0e0e0 !important;
        border-radius: 0 0 8px 0 !important;
    }

    [data-testid="collapsedControl"] button {
        background-color: #ffffff !important;
        color: #1a73e8 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="collapsedControl"] button:hover {
        background-color: #e8f0fe !important;
        border-color: #1a73e8 !important;
        transform: scale(1.05) !important;
    }

    /* 侧边栏内的收起按钮 */
    [data-testid="stSidebar"] button[kind="header"] {
        color: #5f6368 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] button[kind="header"]:hover {
        background-color: #e8eaed !important;
    }


    /* 侧边栏展开时的样式 */
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    /* 侧边栏标题样式 */
    [data-testid="stSidebar"] h1 {
        color: #1a73e8 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #202124 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
        padding-left: 0.5rem !important;
    }

    /* 侧边栏expander样式 */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-weight: 500 !important;
        color: #202124 !important;
        border: 1px solid #e0e0e0 !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background-color: #e8f0fe !important;
        border-color: #1a73e8 !important;
    }

    [data-testid="stSidebar"] details[open] .streamlit-expanderHeader {
        background-color: #e8f0fe !important;
        border-color: #1a73e8 !important;
    }

    /* 侧边栏选择框和滑块样式 */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider {
        margin-bottom: 1rem !important;
    }

    /* 侧边栏按钮样式 */
    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        border: 1px solid #e0e0e0 !important;
    }

    [data-testid="stSidebar"] button:hover {
        background-color: #e8eaed !important;
        border-color: #d0d0d0 !important;
    }

    /* 侧边栏分隔线样式 */
    [data-testid="stSidebar"] hr {
        margin: 1rem 0 !important;
        border-color: #e0e0e0 !important;
        opacity: 0.5 !important;
    }

    /* 侧边栏info框样式 */
    [data-testid="stSidebar"] .stAlert {
        background-color: #e8f0fe !important;
        border-left: 4px solid #1a73e8 !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
    }

    /* 侧边栏文本输入框样式 */
    [data-testid="stSidebar"] textarea {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stSidebar"] textarea:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 1px #1a73e8 !important;
    }

    /* 主内容区域样式 */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* 标题样式 */
    h1 {
        color: #202124 !important;
        font-weight: 400 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
        margin-top: 5rem !important;
    }

    /* 胶囊型输入框 */
    .stTextInput > div > div > input {
        background-color: #f0f4f9 !important;
        color: #202124 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 20px 24px !important;
        font-size: 16px !important;
        height: 60px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        line-height: 60px !important;
        vertical-align: middle !important;
    }

    .stTextInput > div > div > input:focus {
        outline: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        background-color: #e8f0fe !important;
    }

    .stTextInput > div > div > input::placeholder {
        text-align: left !important;
        line-height: 60px !important;
    }

    /* 隐藏输入框 label */
    .stTextInput > label {
        display: none !important;
    }

    /* 输入框容器，减少底部间距 */
    .stTextInput {
        margin-bottom: 0px !important;
    }

    /* 输入框和按钮之间的容器减少间距 */
    .stTextInput + div {
        margin-top: -16px !important;
        padding-top: 8px !important;
    }

    /* 输入框的父容器 */
    div:has(> .stTextInput) {
        margin-bottom: -8px !important;
    }

    /* 小按钮样式（加号、模式、上箭头） */
    .small-button button {
        background-color: #f0f4f9 !important;
        color: #5f6368 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        height: 44px !important;
        min-width: 44px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease !important;
    }

    .small-button button:hover {
        background-color: #e8f0fe !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }

    /* 展开区域样式 */
    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }

    .stExpander > div > div {
        background-color: #f0f4f9 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    /* 文件上传器样式 */
    .stFileUploader {
        background-color: transparent !important;
    }

    /* 图片展示优化 */
    .stImage {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* 按钮容器 */
    [data-testid="column"] {
        padding: 0 2px !important;
        gap: 0px !important;
    }

    /* 按钮行容器减少顶部间距 */
    .row-widget.stHorizontal {
        gap: 2px !important;
        margin-top: 4px !important;
    }

    /* 小按钮容器之间减少间距 */
    .small-button {
        margin: 0 !important;
        padding: 0 !important;
        display: inline-block !important;
    }

    .small-button button {
        margin: 0 2px !important;
    }

    /* 强制减少列间距 */
    div[data-testid="column"] > div {
        padding: 0 !important;
    }

    /* 强制减少按钮之间的间距 */
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
    }

    /* 按钮行紧凑布局 */
    div[data-testid="column"]:has(.small-button) {
        padding: 0 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "current_config" not in st.session_state:
    st.session_state.current_config = {}
if "selected_image_idx" not in st.session_state:
    st.session_state.selected_image_idx = None
if "show_upload_voice" not in st.session_state:
    st.session_state.show_upload_voice = False
if "thinking_mode" not in st.session_state:
    st.session_state.thinking_mode = True
if "show_asset_manager" not in st.session_state:
    st.session_state.show_asset_manager = False

# 获取 API Key
api_key = os.getenv("GOOGLE_API_KEY")

# ========== 侧边栏：控制台 ==========
with st.sidebar:
    st.title("🎛️ Control Panel")
    st.markdown("---")

    # 📂 第一组：生成设置 (默认展开)
    with st.expander("📂 生成设置 (Generation Settings)", expanded=True):
        # 海报比例
        aspect_ratio = st.selectbox(
            "海报比例",
            options=["9:16", "16:9", "1:1", "3:4", "4:3"],
            index=0,
            help="选择海报的宽高比"
        )

        # 生成数量
        num_images = st.slider(
            "生成数量",
            min_value=1,
            max_value=10,
            value=1,
            help="一次生成的海报数量"
        )

    # 🎨 第二组：风格库
    with st.expander("🎨 风格库 (Style Library)", expanded=False):
        # 预设风格
        preset_style = st.selectbox(
            "预设风格",
            options=[
                "自动匹配 (Auto)",
                "极简主义 (Minimalist)",
                "赛博朋克 (Cyberpunk)",
                "商务科技 (Tech Corporate)",
                "温暖手绘 (Warm Illustration)"
            ],
            index=0,
            help="选择预设的设计风格"
        )

        # 风格强度
        style_strength = st.slider(
            "风格强度",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="控制风格应用的强度，0为弱，1为强"
        )

        st.divider()

        # 已保存的自定义风格
        st.caption("📚 自定义风格")
        saved_styles = style_manager.list_styles()
        if saved_styles:
            style_names = ["不使用"] + [s["name"] for s in saved_styles]
            selected_custom_style = st.selectbox(
                "自定义风格",
                style_names,
                label_visibility="collapsed"
            )
        else:
            selected_custom_style = "不使用"
            st.caption("暂无自定义风格")

    # 🧩 第三组：素材管理
    with st.expander("🧩 素材管理 (Assets)", expanded=False):
        # Logo/水印上传
        uploaded_logo = st.file_uploader(
            "上传 Logo/水印",
            type=["png", "jpg", "jpeg"],
            help="上传品牌Logo或水印图片"
        )

        # 自动添加 Logo
        auto_add_logo = st.checkbox(
            "自动添加 Logo",
            value=False,
            help="自动在生成的海报上添加Logo"
        )

        st.divider()

        # 二维码上传
        uploaded_qr = st.file_uploader(
            "上传二维码",
            type=["png", "jpg", "jpeg"],
            help="上传二维码图片"
        )

        # 素材管理按钮
        if st.button("📁 管理素材库", use_container_width=True):
            st.session_state.show_asset_manager = not st.session_state.show_asset_manager

    # ⚙️ 第四组：高级配置
    with st.expander("⚙️ 高级配置 (Advanced)", expanded=False):
        # 负向提示词
        negative_prompt = st.text_area(
            "负向提示词 (Negative Prompt)",
            placeholder="例如：模糊、低质量、变形...",
            help="指定不希望出现在海报中的元素"
        )

        st.divider()

        # 模型版本显示
        st.caption("🤖 当前模型")
        st.info("**Gemini 3 Pro**")

        # Thinking模式
        thinking_mode_sidebar = st.checkbox(
            "启用 Thinking 模式",
            value=st.session_state.thinking_mode,
            help="AI会深度思考设计方案，质量更高但速度较慢"
        )
        st.session_state.thinking_mode = thinking_mode_sidebar

# ========== 主界面 ==========

# 主标题
st.markdown("# MirrorPost AI")

# 素材管理界面
if st.session_state.show_asset_manager:
    st.markdown("### 🛠️ 素材管理")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Logo 管理")
        logo_upload = st.file_uploader("上传 Logo", type=["png", "jpg", "jpeg"], key="logo_upload")
        if logo_upload:
            logo_img = Image.open(logo_upload)
            st.image(logo_img, caption="Logo 预览", width=150)
            if st.button("保存 Logo"):
                asset_manager.save_logo(logo_img)
                st.success("✅ Logo 已保存")
                st.rerun()

        # 显示已有 Logo
        logos = asset_manager.list_logos()
        if logos:
            for logo_name in logos:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.caption(f"📷 {logo_name}")
                with col_b:
                    if st.button("删除", key=f"del_logo_{logo_name}"):
                        asset_manager.delete_logo(logo_name)
                        st.rerun()

    with col2:
        st.subheader("二维码管理")
        qr_upload = st.file_uploader("上传二维码", type=["png", "jpg", "jpeg"], key="qr_upload")
        if qr_upload:
            qr_img = Image.open(qr_upload)
            st.image(qr_img, caption="二维码预览", width=150)
            if st.button("保存二维码"):
                asset_manager.save_qrcode(qr_img)
                st.success("✅ 二维码已保存")
                st.rerun()

        # 显示已有二维码
        qrcodes = asset_manager.list_qrcodes()
        if qrcodes:
            for qr_name in qrcodes:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.caption(f"📷 {qr_name}")
                with col_b:
                    if st.button("删除", key=f"del_qr_{qr_name}"):
                        asset_manager.delete_qrcode(qr_name)
                        st.rerun()

    st.divider()

# ========== 输入区域 ==========

# 胶囊型输入框
user_prompt = st.text_input(
    "",
    placeholder="请输入您想生成海报的要求，如：风格、元素、文案……",
    key="main_prompt_input"
)

# 按钮组布局（减少间距）
col_left, col_spacer, col_right = st.columns([0.6, 6, 1.4], gap="small")

with col_left:
    # 加号按钮（折叠上传和语音功能）
    st.markdown('<div class="small-button">', unsafe_allow_html=True)
    if st.button("➕", key="toggle_upload"):
        st.session_state.show_upload_voice = not st.session_state.show_upload_voice
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # 右侧按钮组：模式按钮 + 上箭头生成按钮（减少间距）
    btn_col1, btn_col2 = st.columns([1, 1], gap="small")

    with btn_col1:
        # 模式切换按钮
        st.markdown('<div class="small-button">', unsafe_allow_html=True)
        mode_label = "🧠" if st.session_state.thinking_mode else "⚡"
        if st.button(mode_label, key="toggle_mode", help="切换 Thinking/Fast 模式"):
            st.session_state.thinking_mode = not st.session_state.thinking_mode
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with btn_col2:
        # 生成按钮（上箭头）
        st.markdown('<div class="small-button">', unsafe_allow_html=True)
        generate_button = st.button("↑", key="generate_btn", help="生成海报")
        st.markdown('</div>', unsafe_allow_html=True)

# 上传和语音功能区域（折叠）
reference_image = None
if st.session_state.show_upload_voice:
    st.markdown("<br>", unsafe_allow_html=True)

    upload_col1, upload_col2 = st.columns(2)

    with upload_col1:
        st.caption("📷 上传参考图片")
        uploaded_image = st.file_uploader(
            "图片",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            key="image_upload"
        )
        if uploaded_image:
            reference_image = Image.open(uploaded_image)
            st.image(reference_image, width=150)

    with upload_col2:
        st.caption("🎤 语音输入")
        audio_bytes = st.audio_input("语音", label_visibility="collapsed")
        if audio_bytes:
            st.caption("⚠️ 需要 Speech API")

# 生成逻辑
if generate_button:
    if not user_prompt:
        st.warning("⚠️ 请先输入海报描述")
    elif not api_key:
        st.error("❌ 请先在 .env 文件中设置 GOOGLE_API_KEY")
    else:
        try:
            # 构建完整的提示词
            final_prompt = user_prompt

            # 添加预设风格关键词
            style_keywords = {
                "自动匹配 (Auto)": "",
                "极简主义 (Minimalist)": "minimalist design, clean layout, simple geometric shapes, plenty of white space",
                "赛博朋克 (Cyberpunk)": "cyberpunk style, neon colors, futuristic elements, tech-inspired, dark background with bright accents",
                "商务科技 (Tech Corporate)": "professional business style, modern tech aesthetic, corporate colors, clean and sophisticated",
                "温暖手绘 (Warm Illustration)": "warm hand-drawn illustration style, friendly and approachable, soft colors, artistic touch"
            }

            # 拼接风格关键词
            if preset_style != "自动匹配 (Auto)" and style_keywords.get(preset_style):
                style_keyword = style_keywords[preset_style]
                final_prompt = f"{user_prompt}. Style: {style_keyword}. Style strength: {style_strength}"

            # 获取自定义风格提示词
            custom_style_prompt = None
            if selected_custom_style != "不使用":
                selected_style = style_manager.load_style(selected_custom_style)
                if selected_style:
                    custom_style_prompt = selected_style.get("user_prompt")
                    if custom_style_prompt:
                        final_prompt = f"{final_prompt}. {custom_style_prompt}"

            # 添加负向提示词（如果有）
            if negative_prompt:
                final_prompt = f"{final_prompt}. Avoid: {negative_prompt}"

            # 加载素材
            logo_image = None
            qrcode_image = None

            # 如果上传了新的Logo，使用上传的
            if uploaded_logo:
                logo_image = Image.open(uploaded_logo)
            elif auto_add_logo:
                # 否则使用素材库中的第一个Logo
                logos = asset_manager.list_logos()
                if logos:
                    logo_image = asset_manager.load_logo(logos[0])

            # 如果上传了新的二维码，使用上传的
            if uploaded_qr:
                qrcode_image = Image.open(uploaded_qr)
            else:
                # 否则使用素材库中的第一个二维码
                qrcodes = asset_manager.list_qrcodes()
                if qrcodes:
                    qrcode_image = asset_manager.load_qrcode(qrcodes[0])

            # 生成提示
            thinking_mode = st.session_state.thinking_mode
            spinner_text = "AI 正在思考设计方案并绘图..." if thinking_mode else "AI 正在快速生成海报..."

            with st.spinner(spinner_text):
                # 调用后端批量生成
                generated_images = generate_posters(
                    user_prompt=final_prompt,
                    aspect_ratio=aspect_ratio,
                    num_images=num_images,
                    thinking_mode=thinking_mode,
                    reference_image=reference_image,
                    style_prompt=None,  # 已经拼接到final_prompt中
                    logo_image=logo_image,
                    qrcode_image=qrcode_image
                )

            # 保存到 session state
            st.session_state.generated_images = generated_images
            st.session_state.current_prompt = user_prompt
            st.session_state.current_config = {
                "aspect_ratio": aspect_ratio,
                "thinking_mode": thinking_mode
            }

            st.success(f"✅ 成功生成 {len(generated_images)} 张海报！")
            st.info("💾 所有海报已保存至 `generated_posters/` 文件夹")

        except ValueError as e:
            st.error(f"❌ 配置错误: {str(e)}")
        except Exception as e:
            st.error(f"❌ 生成失败: {str(e)}")
            st.caption("请检查网络连接或 API Key 是否有效")

# 展示生成结果 - 网格布局
if st.session_state.generated_images:
    st.divider()
    st.markdown("### 🖼️ 生成结果")

    # 网格展示（每行 4 张）
    cols_per_row = 4
    images = st.session_state.generated_images

    for i in range(0, len(images), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(images):
                with col:
                    st.image(images[i + j], use_container_width=True)

                    # 按钮行
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        # 查看大图按钮
                        if st.button(f"🔍", key=f"view_{i+j}", help="查看大图"):
                            st.session_state.selected_image_idx = i + j

                    with btn_col2:
                        # 保存风格按钮
                        if st.button(f"💾", key=f"save_{i+j}", help="存为风格"):
                            st.session_state[f"save_style_{i+j}"] = True

    # 继续优化输入框
    st.divider()
    st.markdown("### 🔄 继续优化")
    st.caption("不满意？告诉我需要调整什么")

    refine_prompt = st.text_input(
        "输入优化指令",
        placeholder="例如：换个亮一点的颜色、更有科技感、加大文字",
        key="refine_input"
    )

    if st.button("⚡ 重新生成", type="secondary", use_container_width=True):
        if refine_prompt:
            try:
                # 合并原始提示词和优化指令
                combined_prompt = f"{st.session_state.current_prompt}. {refine_prompt}"

                # 应用风格配置
                final_refine_prompt = combined_prompt

                # 添加预设风格关键词
                style_keywords = {
                    "自动匹配 (Auto)": "",
                    "极简主义 (Minimalist)": "minimalist design, clean layout, simple geometric shapes, plenty of white space",
                    "赛博朋克 (Cyberpunk)": "cyberpunk style, neon colors, futuristic elements, tech-inspired, dark background with bright accents",
                    "商务科技 (Tech Corporate)": "professional business style, modern tech aesthetic, corporate colors, clean and sophisticated",
                    "温暖手绘 (Warm Illustration)": "warm hand-drawn illustration style, friendly and approachable, soft colors, artistic touch"
                }

                if preset_style != "自动匹配 (Auto)" and style_keywords.get(preset_style):
                    style_keyword = style_keywords[preset_style]
                    final_refine_prompt = f"{combined_prompt}. Style: {style_keyword}. Style strength: {style_strength}"

                # 获取自定义风格
                if selected_custom_style != "不使用":
                    selected_style = style_manager.load_style(selected_custom_style)
                    if selected_style:
                        custom_style_prompt = selected_style.get("user_prompt")
                        if custom_style_prompt:
                            final_refine_prompt = f"{final_refine_prompt}. {custom_style_prompt}"

                # 添加负向提示词
                if negative_prompt:
                    final_refine_prompt = f"{final_refine_prompt}. Avoid: {negative_prompt}"

                # 加载素材
                logo_image = None
                qrcode_image = None

                if uploaded_logo:
                    logo_image = Image.open(uploaded_logo)
                elif auto_add_logo:
                    logos = asset_manager.list_logos()
                    if logos:
                        logo_image = asset_manager.load_logo(logos[0])

                if uploaded_qr:
                    qrcode_image = Image.open(uploaded_qr)
                else:
                    qrcodes = asset_manager.list_qrcodes()
                    if qrcodes:
                        qrcode_image = asset_manager.load_qrcode(qrcodes[0])

                spinner_text = "AI 正在根据你的反馈重新生成..."

                with st.spinner(spinner_text):
                    # 重新生成
                    generated_images = generate_posters(
                        user_prompt=final_refine_prompt,
                        aspect_ratio=aspect_ratio,
                        num_images=num_images,
                        thinking_mode=st.session_state.thinking_mode,
                        reference_image=reference_image,
                        style_prompt=None,
                        logo_image=logo_image,
                        qrcode_image=qrcode_image
                    )

                # 更新 session state
                st.session_state.generated_images = generated_images
                st.session_state.current_prompt = combined_prompt
                st.success(f"✅ 已根据反馈重新生成 {len(generated_images)} 张海报！")
                st.rerun()

            except Exception as e:
                st.error(f"❌ 重新生成失败: {str(e)}")
        else:
            st.warning("⚠️ 请输入优化指令")

    # 风格保存对话框
    for idx in range(len(images)):
        if st.session_state.get(f"save_style_{idx}", False):
            with st.form(key=f"style_form_{idx}"):
                st.subheader(f"保存风格 - 海报 #{idx+1}")
                style_name = st.text_input("风格名称", key=f"name_{idx}")
                style_desc = st.text_area("风格描述（可选）", key=f"desc_{idx}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("保存"):
                        if style_name:
                            style_manager.save_style(
                                name=style_name,
                                user_prompt=st.session_state.current_prompt,
                                aspect_ratio=st.session_state.current_config["aspect_ratio"],
                                thinking_mode=st.session_state.current_config["thinking_mode"],
                                description=style_desc
                            )
                            st.success(f"✅ 风格 '{style_name}' 已保存")
                            st.session_state[f"save_style_{idx}"] = False
                            st.rerun()
                        else:
                            st.warning("请输入风格名称")
                with col2:
                    if st.form_submit_button("取消"):
                        st.session_state[f"save_style_{idx}"] = False
                        st.rerun()

    # 大图查看对话框
    if st.session_state.selected_image_idx is not None:
        idx = st.session_state.selected_image_idx
        if idx < len(images):
            st.divider()
            st.markdown(f"### 🔍 海报预览 #{idx+1}")

            col_img, col_tune = st.columns([3, 1])

            with col_img:
                # 显示大图
                st.image(images[idx], use_container_width=True)

            with col_tune:
                st.markdown("#### 🎨 微调选项")

                # 颜色调整
                st.caption("**颜色**")
                color_adjustment = st.radio(
                    "颜色调整",
                    ["保持原样", "更亮", "更暗", "更鲜艳", "更柔和"],
                    key="color_adj",
                    label_visibility="collapsed"
                )

                st.divider()

                # 风格调整
                st.caption("**风格**")
                style_adjustment = st.radio(
                    "风格调整",
                    ["保持原样", "更简洁", "更复杂", "更现代", "更经典"],
                    key="style_adj",
                    label_visibility="collapsed"
                )

                st.divider()

                # 文字调整
                st.caption("**文字**")
                text_adjustment = st.radio(
                    "文字调整",
                    ["保持原样", "文字更大", "文字更小", "字体更粗", "字体更细"],
                    key="text_adj",
                    label_visibility="collapsed"
                )

                st.divider()

                # 自定义微调
                custom_tune = st.text_area(
                    "自定义微调",
                    placeholder="输入其他调整需求...",
                    key="custom_tune"
                )

                st.divider()

                # 微调按钮
                if st.button("✨ 应用微调", type="primary", use_container_width=True):
                    # 构建微调提示词
                    tune_parts = []
                    if color_adjustment != "保持原样":
                        tune_parts.append(color_adjustment)
                    if style_adjustment != "保持原样":
                        tune_parts.append(style_adjustment)
                    if text_adjustment != "保持原样":
                        tune_parts.append(text_adjustment)
                    if custom_tune:
                        tune_parts.append(custom_tune)

                    if tune_parts:
                        try:
                            # 合并提示词
                            tune_instruction = ", ".join(tune_parts)
                            tuned_prompt = f"{st.session_state.current_prompt}. Apply these adjustments: {tune_instruction}"

                            # 应用风格配置
                            final_tuned_prompt = tuned_prompt

                            # 添加预设风格关键词
                            style_keywords = {
                                "自动匹配 (Auto)": "",
                                "极简主义 (Minimalist)": "minimalist design, clean layout, simple geometric shapes, plenty of white space",
                                "赛博朋克 (Cyberpunk)": "cyberpunk style, neon colors, futuristic elements, tech-inspired, dark background with bright accents",
                                "商务科技 (Tech Corporate)": "professional business style, modern tech aesthetic, corporate colors, clean and sophisticated",
                                "温暖手绘 (Warm Illustration)": "warm hand-drawn illustration style, friendly and approachable, soft colors, artistic touch"
                            }

                            if preset_style != "自动匹配 (Auto)" and style_keywords.get(preset_style):
                                style_keyword = style_keywords[preset_style]
                                final_tuned_prompt = f"{tuned_prompt}. Style: {style_keyword}. Style strength: {style_strength}"

                            # 获取自定义风格
                            if selected_custom_style != "不使用":
                                selected_style = style_manager.load_style(selected_custom_style)
                                if selected_style:
                                    custom_style_prompt = selected_style.get("user_prompt")
                                    if custom_style_prompt:
                                        final_tuned_prompt = f"{final_tuned_prompt}. {custom_style_prompt}"

                            # 添加负向提示词
                            if negative_prompt:
                                final_tuned_prompt = f"{final_tuned_prompt}. Avoid: {negative_prompt}"

                            # 加载素材
                            logo_image = None
                            qrcode_image = None

                            if uploaded_logo:
                                logo_image = Image.open(uploaded_logo)
                            elif auto_add_logo:
                                logos = asset_manager.list_logos()
                                if logos:
                                    logo_image = asset_manager.load_logo(logos[0])

                            if uploaded_qr:
                                qrcode_image = Image.open(uploaded_qr)
                            else:
                                qrcodes = asset_manager.list_qrcodes()
                                if qrcodes:
                                    qrcode_image = asset_manager.load_qrcode(qrcodes[0])

                            with st.spinner("正在应用微调..."):
                                # 只生成一张微调后的海报
                                tuned_images = generate_posters(
                                    user_prompt=final_tuned_prompt,
                                    aspect_ratio=aspect_ratio,
                                    num_images=1,
                                    thinking_mode=st.session_state.thinking_mode,
                                    reference_image=images[idx],  # 使用当前图片作为参考
                                    style_prompt=None,
                                    logo_image=logo_image,
                                    qrcode_image=qrcode_image
                                )

                            if tuned_images:
                                # 替换当前图片
                                st.session_state.generated_images[idx] = tuned_images[0]
                                st.success("✅ 微调已应用")
                                st.rerun()

                        except Exception as e:
                            st.error(f"❌ 微调失败: {str(e)}")
                    else:
                        st.warning("⚠️ 请选择至少一项调整")

            # 关闭按钮
            if st.button("✖️ 关闭预览", key="close_preview"):
                st.session_state.selected_image_idx = None
                st.rerun()

# 页脚
st.divider()
st.caption("Powered by Google Gemini 3 Pro | MirrorPost AI v2.0")

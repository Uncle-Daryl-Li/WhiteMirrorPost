# 测试侧边栏显示
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="侧边栏测试",
    page_icon="🎛️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS样式
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }

    [data-testid="stSidebar"] h1 {
        color: #1a73e8 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("🎛️ Control Panel")
    st.markdown("---")

    with st.expander("📂 生成设置", expanded=True):
        st.selectbox("海报比例", ["9:16", "16:9", "1:1"])
        st.slider("生成数量", 1, 4, 1)

    with st.expander("🎨 风格库", expanded=False):
        st.selectbox("预设风格", ["自动匹配", "极简主义", "赛博朋克"])
        st.slider("风格强度", 0.0, 1.0, 0.7)

    with st.expander("🧩 素材管理", expanded=False):
        st.file_uploader("上传 Logo/水印", type=["png", "jpg"])
        st.checkbox("自动添加 Logo")

    with st.expander("⚙️ 高级配置", expanded=False):
        st.text_area("负向提示词", placeholder="例如：模糊、低质量...")
        st.info("**Gemini 3 Pro**")

# 主界面
st.markdown("# 测试页面")
st.write("如果你能看到左侧的控制台，说明侧边栏正常工作！")

if st.button("✅ 测试按钮"):
    st.success("按钮点击成功！侧边栏功能正常！")

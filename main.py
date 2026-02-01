import streamlit as st
import os
from dotenv import load_dotenv
from core.llm_factory import LLMFactory
from engines.sql_engine import SQLEngine
from engines.vector_engine import VectorEngine
from core.agent_manager import AgentManager

# 1. Load cấu hình từ file .env
load_dotenv()

# 2. Cấu hình trang & Ẩn Menu
st.set_page_config(page_title="Tiệm Vàng AI Manager", layout="wide", page_icon="💎")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# 3. Khởi tạo Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# 4. Sidebar: Cấu hình
with st.sidebar:
    st.title("💎 Vũ Nghi Xuân AI")
    st.divider()

    st.subheader("🤖 Bộ não AI")
    default_p = os.getenv("DEFAULT_PROVIDER", "Ollama").capitalize()

    # Thêm hàm callback hoặc để nó tự rerun khi thay đổi
    provider = st.selectbox(
        "Nhà cung cấp", 
        ["Ollama", "Gemini", "Groq"], 
        index=["Ollama", "Gemini", "Groq"].index(default_p)
    )
        
    default_model = os.getenv(f"{provider.upper()}_MODEL")
    model_name = st.text_input("Model Name", value=default_model)
    
    st.divider()

    # --- LỚP BẢO MẬT ADMIN ---
    st.subheader("🔐 Quản trị")
    pwd = st.text_input("Mật khẩu Admin:", type="password")
    if pwd == "admin123":
        st.session_state.is_admin = True
        st.success("Xác thực thành công!")
        if st.button("⚙️ Vào trang Cấu hình Hệ thống", use_container_width=True):
            st.switch_page("pages/admin.py")

# 5. Khởi tạo Dữ liệu
sql_path = os.getenv("SQL_DATA_PATH", "data/gia_vang.xlsx")
vector_path = os.getenv("VECTOR_DATA_PATH", "data/chinh_sach/")

@st.cache_resource
def init_engines():
    return SQLEngine(sql_path), VectorEngine(vector_path)

sql_eng, vec_eng = init_engines()

# ---------------------------------------------------------
# 6. TỰ ĐỘNG KÍCH HOẠT AGENT KHI THÔNG SỐ THAY ĐỔI
# ---------------------------------------------------------
# Chúng ta dùng key để kiểm tra nếu config thay đổi thì tạo lại agent
config_key = f"{provider}_{model_name}"

if "current_config" not in st.session_state or st.session_state.current_config != config_key:
    try:
        env_key = os.getenv(f"{provider.upper()}_API_KEY")
        llm = LLMFactory.get_llm(provider, model_name, env_key)
        st.session_state.agent = AgentManager(llm, sql_eng, vec_eng)
        st.session_state.current_config = config_key
        # Không cần dùng st.success ở đây để tránh hiện thông báo liên tục mỗi lần load
    except Exception as e:
        st.sidebar.error(f"Lỗi kết nối {provider}: {e}")

# ---------------------------------------------------------

st.title("🤖 Trợ Lý Nghiệp Vụ Đa Dữ Liệu")
if "agent" in st.session_state:
    st.caption(f"🚀 Hệ thống sẵn sàng | Model: **{provider} - {model_name}**")

st.divider()

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý nhập liệu
if prompt := st.chat_input("Hỏi về giá vàng hoặc quy trình bảo hành..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "agent" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("Đang tra cứu dữ liệu..."):
                try:
                    response = st.session_state.agent.solve(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Lỗi khi xử lý câu hỏi: {e}")
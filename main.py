"""
main.py (Giao diện Streamlit)
Anh cài thư viện: pip install streamlit langchain pandas openpyxl
"""

import streamlit as st
from core.llm_factory import LLMFactory
from engines.sql_engine import SQLEngine
from engines.vector_engine import VectorEngine
from core.agent_manager import AgentManager

st.set_page_config(page_title="Tiệm Vàng AI Manager", layout="wide")

st.title("🤖 Hệ Thống Chat Nghiệp Vụ Đa Dữ Liệu")

# Sidebar cấu hình
with st.sidebar:
    st.header("Cấu hình hệ thống")
    provider = st.selectbox("Chọn LLM", ["Gemini", "Groq", "Ollama"])
    model_name = st.text_input("Model Name", value="gemini-1.5-flash" if provider == "Gemini" else "llama3-8b")
    api_key = st.text_input("API Key (nếu có)", type="password")
    
    st.divider()
    st.info("Hệ thống đang kết nối: Excel (Giá vàng) & Docs (Chính sách)")

# Khởi tạo Engines và Agent
sql_eng = SQLEngine("data/gia_vang.xlsx")
vec_eng = VectorEngine("data/chinh_sach/")

if st.button("Khởi động Agent"):
    try:
        llm = LLMFactory.get_llm(provider, model_name, api_key)
        st.session_state.agent = AgentManager(llm, sql_eng, vec_eng)
        st.success("Agent đã sẵn sàng!")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Giao diện Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi về giá vàng hoặc chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "agent" in st.session_state:
        response = st.session_state.agent.solve(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        st.warning("Vui lòng nhấn 'Khởi động Agent' ở bên trái trước.")
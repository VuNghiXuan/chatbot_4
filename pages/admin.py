import streamlit as st

st.set_page_config(page_title="Quản trị Hệ thống", layout="wide")

# Kiểm tra quyền truy cập (từ session_state ở main.py)
if not st.session_state.get("is_admin", False):
    st.error("Bạn không có quyền truy cập trang này!")
    if st.button("Quay lại trang chủ"):
        st.switch_page("main.py")
    st.stop()

st.title("⚙️ Cấu hình Hệ thống Admin")
st.write("Chào mừng Vũ Nghi Xuân. Đây là nơi anh quản lý dữ liệu và cấu hình.")

if st.button("🏠 Quay lại Chat"):
    st.switch_page("main.py")
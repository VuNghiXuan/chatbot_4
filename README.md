# 💎 Tiệm Vàng AI Manager (Multi-Engine RAG System)

# Hệ thống trợ lý ảo thông minh dành cho tiệm vàng, có khả năng xử lý đồng thời dữ liệu số liệu (Giá vàng, Giao dịch) từ Excel/SQL và dữ liệu văn bản (Quy định, Chính sách) từ PDF/Word.

# 

# 🌟 Tính năng nổi bật

# Semantic Routing: Tự động phân tích câu hỏi để quyết định khi nào cần tra cứu bảng biểu, khi nào cần tìm kiếm văn bản quy trình.

# 

# Hybrid Data Processing:

# 

# SQL Engine: Trích xuất chính xác dữ liệu từ file Excel/CSV (hỗ trợ mở rộng lên SQL Server).

# 

# Vector Engine: Sử dụng FAISS và HuggingFace Embeddings để tìm kiếm ngữ nghĩa trong các tài liệu nghiệp vụ.

# 

# LLM Factory: Linh hoạt chuyển đổi giữa các "bộ não" AI hàng đầu: Gemini (Google), Groq (Llama3), hoặc chạy nội bộ hoàn toàn với Ollama.

# 

# Multi-tasking Prompt: Khả năng tổng hợp dữ liệu từ nhiều nguồn để đưa ra câu trả lời cuối cùng chính xác và thân thiện.

# 

# 🏗 Cấu trúc thư mục

# Plaintext

# chatbot\_4/

# ├── main.py                 # Giao diện chính Streamlit

# ├── core/

# │   ├── llm\_factory.py      # Quản lý khởi tạo các mô hình AI

# │   └── agent\_manager.py    # Bộ não điều phối toàn bộ hệ thống

# ├── engines/

# │   ├── base\_engine.py      # Lớp trừu tượng (Abstract Base Class)

# │   ├── sql\_engine.py       # Xử lý dữ liệu bảng biểu (Excel/CSV)

# │   └── vector\_engine.py    # Xử lý dữ liệu văn bản (FAISS)

# ├── utils/

# │   └── router.py           # Phân loại ý định người dùng

# ├── data/

# │   ├── gia\_vang.xlsx       # Dữ liệu số liệu đầu vào

# │   └── chinh\_sach/         # Thư mục chứa file PDF/Word quy trình

# └── requirements.txt        # Danh sách thư viện cần thiết

# 🚀 Hướng dẫn cài đặt

# Clone dự án:

# 

# Bash

# git clone https://github.com/VuNghiXuan/chatbot\_4.git

# cd chatbot\_4

# Cài đặt môi trường ảo:

# 

# Bash

# python -m venv env

# source env/bin/scripts/activate  # Windows: env\\Scripts\\activate

# Cài đặt thư viện:

# 

# Bash

# pip install streamlit langchain-community langchain-google-genai langchain-groq pandas openpyxl faiss-cpu sentence-transformers unstructured python-docx pypdf

# 🛠 Cách sử dụng

# Chuẩn bị dữ liệu:

# 

# Để file báo cáo/giá vàng vào data/gia\_vang.xlsx.

# 

# Để các file quy định bảo hành, chính sách vào thư mục data/chinh\_sach/.

# 

# Khởi chạy ứng dụng:

# 

# Bash

# streamlit run main.py

# Thao tác trên giao diện:

# 

# Chọn nhà cung cấp LLM (Gemini, Groq hoặc Ollama).

# 

# Nhập API Key tương ứng.

# 

# Nhấn "Khởi động Agent" để hệ thống nạp dữ liệu vào bộ nhớ.

# 

# Bắt đầu đặt câu hỏi (VD: "Giá vàng 18k hôm nay bao nhiêu và chính sách thu mua thế nào?").

# 

# 🧠 Cơ chế hoạt động

# Nhận câu hỏi: Người dùng nhập câu hỏi vào Chat.

# 

# Phân tuyến (Routing): SemanticRouter nhận diện từ khóa để biết khách đang hỏi về giá hay về chính sách.

# 

# Trích xuất (Retrieval):

# 

# SQLEngine lọc các dòng dữ liệu liên quan trong Excel.

# 

# VectorEngine tìm kiếm các đoạn văn bản tương đồng nhất trong PDF/Word.

# 

# Tổng hợp (Augmentation): Toàn bộ dữ liệu thô được đưa vào một Prompt chuyên dụng.

# 

# Trả lời (Generation): LLM đọc hiểu dữ liệu và trả lời khách hàng theo phong cách chuyên nghiệp.

# 

# 📝 Lưu ý bảo mật

# Không push file system\_config.json hoặc thư mục env/ lên GitHub.

# 

# API Key nhập trên giao diện chỉ lưu trong session hiện tại, không lưu vĩnh viễn vào code.


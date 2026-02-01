"""
C. Vector Engine (Chuyên trị văn bản: Chính sách, Quy trình)
Dùng để xử lý các file Word/PDF bằng cách tìm kiếm theo ý nghĩa (Vector).
pip install langchain-community faiss-cpu sentence-transformers unstructured python-docx pypdf
"""

import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class VectorEngine:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.vector_db = None
        self._build_index()

    def _build_index(self):
        """Đọc tất cả file trong thư mục và xây dựng bộ chỉ mục Vector"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"Thư mục {self.folder_path} trống. Hãy thêm file Word/PDF vào.")
            return

        # 1. Load các file (Hỗ trợ .docx và .pdf)
        # Loader này sẽ quét toàn bộ thư mục
        loader = DirectoryLoader(self.folder_path, glob="**/*.docx", loader_cls=UnstructuredWordDocumentLoader)
        documents = loader.load()
        
        if not documents:
            # Nếu không có docx, thử tìm PDF
            loader_pdf = DirectoryLoader(self.folder_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
            documents = loader_pdf.load()

        if documents:
            # 2. Chia nhỏ văn bản (Chunking) để AI dễ tìm và không quá dài
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents(documents)

            # 3. Tạo Vector DB và lưu vào bộ nhớ (RAM)
            self.vector_db = FAISS.from_documents(chunks, self.embeddings)
            print(f"--- Đã nạp {len(chunks)} đoạn văn bản từ {self.folder_path} ---")

    def retrieve(self, query: str):
        """Tìm kiếm các đoạn văn bản có ý nghĩa sát nhất với câu hỏi"""
        if not self.vector_db:
            return "Dữ liệu chính sách hiện đang trống."

        # Tìm 3 đoạn văn bản liên quan nhất (k=3)
        docs = self.vector_db.similarity_search(query, k=3)
        
        # Gộp các đoạn văn bản lại thành một context
        context_text = "\n---\n".join([doc.page_content for doc in docs])
        
        return f"[TRÍCH XUẤT CHÍNH SÁCH/QUY ĐỊNH]:\n{context_text}"
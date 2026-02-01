"""
B. SQL Engine (Chuyên trị số liệu: Giá vàng, Giao dịch)
Dùng cho các file Excel hoặc Database. 
Sau này anh đổi từ file Excel sang SQL Server chỉ cần sửa trong Class này.
"""

import pandas as pd
import os

class SQLEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
        """Tải dữ liệu và chuẩn hóa tên cột để dễ truy vấn"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {self.file_path}")
        
        # Đọc file (hỗ trợ cả Excel và CSV)
        if self.file_path.endswith('.xlsx'):
            self.df = pd.read_excel(self.file_path)
        else:
            self.df = pd.read_csv(self.file_path)
        
        # Viết hoa toàn bộ tên cột và xóa khoảng trắng để tránh lỗi lệch tên
        self.df.columns = [str(col).strip().upper() for col in self.df.columns]

    def retrieve(self, query: str):
        """Lọc dữ liệu thông minh dựa trên từ khóa trong câu hỏi"""
        query_l = query.lower()
        
        # 1. Tìm kiếm các dòng liên quan (ví dụ: khách hỏi '18k' thì lọc dòng có '18k')
        # Giả sử file có cột 'LOẠI VÀNG' hoặc 'SẢN PHẨM'
        mask = self.df.apply(lambda row: row.astype(str).str.lower().str.contains(query_l).any(), axis=1)
        filtered_df = self.df[mask]

        if filtered_df.empty:
            # Nếu không lọc được theo từ khóa, trả về 5 dòng mới nhất để AI có dữ liệu tham khảo
            context_data = self.df.tail(5).to_string()
            return f"Không tìm thấy dòng cụ thể, đây là dữ liệu mới nhất trong hệ thống:\n{context_data}"
        
        # 2. Chỉ trả về các dòng đã lọc (giúp tiết kiệm token và tăng độ chính xác)
        context_result = filtered_df.to_string()
        
        return f"[KẾT QUẢ TRÍCH XUẤT TỪ FILE SỐ LIỆU]:\n{context_result}"
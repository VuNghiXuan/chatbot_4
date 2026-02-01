"""
Cập nhật file utils/router.py (Để hỗ trợ đa nhiệm)
Hàm cũ chỉ trả về 1 chuỗi, 
hàm mới sẽ trả về một list các công cụ cần thiết:
"""


class SemanticRouter:
    @staticmethod
    def guide_multi(query: str):
        q = query.lower()
        needed_routes = []
        
        # Kiểm tra vế về số liệu
        if any(word in q for word in ["giá", "tiền", "mua", "bán", "giao dịch", "báo cáo"]):
            needed_routes.append("SQL")
            
        # Kiểm tra vế về chính sách/kiến thức
        if any(word in q for word in ["quy định", "chính sách", "làm sao", "thế nào", "bảo hành"]):
            needed_routes.append("VECTOR")
            
        # Nếu không khớp cái nào, mặc định dùng Vector để trả lời tư vấn chung
        if not needed_routes:
            needed_routes.append("VECTOR")
            
        return list(set(needed_routes)) # Xóa trùng lặp
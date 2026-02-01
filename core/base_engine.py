"""
base_engine.py

A. Base Engine (Lớp nền tảng)
Lớp này định nghĩa "luật chơi" chung. 
Mọi bộ máy tìm kiếm sau này (dù là tìm trong PDF hay SQL) đều phải tuân theo cấu trúc này.
"""



from abc import ABC, abstractmethod

class BaseEngine(ABC):
    @abstractmethod
    def retrieve(self, query: str):
        """Mọi engine đều phải có hàm lấy dữ liệu"""
        pass
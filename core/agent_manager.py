"""
3. Agent Manager - "Ông chủ" điều phối
Đây là nơi quan trọng nhất. 
Nó sử dụng một bộ Router để biết câu hỏi nào thì gọi "nhân viên" (Engine) nào.
"""

from utils.router import SemanticRouter

class AgentManager:
    def __init__(self, llm, sql_engine, vector_engine):
        """
        Dependency Injection: Đưa các công cụ vào cho ông chủ dùng
        """
        self.llm = llm
        self.sql_engine = sql_engine
        self.vector_engine = vector_engine

    def solve(self, query: str):
        # 1. Phân tích ý định (Có thể chứa nhiều ý định cùng lúc)
        # Router giờ đây trả về một danh sách các nghiệp vụ cần dùng
        routes = SemanticRouter.guide_multi(query)
        
        contexts = []
        
        # 2. Thu thập dữ liệu từ tất cả các nguồn liên quan
        if "SQL" in routes:
            try:
                sql_data = self.sql_engine.retrieve(query)
                contexts.append(f"[DỮ LIỆU SỐ LIỆU/BẢNG BIỂU]:\n{sql_data}")
            except Exception as e:
                contexts.append(f"Lỗi truy xuất số liệu: {str(e)}")

        if "VECTOR" in routes:
            try:
                vector_data = self.vector_engine.retrieve(query)
                contexts.append(f"[DỮ LIỆU CHÍNH SÁCH/VĂN BẢN]:\n{vector_data}")
            except Exception as e:
                contexts.append(f"Lỗi truy xuất chính sách: {str(e)}")

        # 3. Kết hợp toàn bộ ngữ cảnh thu được
        full_context = "\n\n".join(contexts)
        
        # 4. Prompt Engineering nâng cao để LLM xử lý đa nhiệm
        prompt = f"""
        Bạn là trợ lý ảo chuyên nghiệp của tiệm vàng. 
        Dựa trên các dữ liệu thực tế thu thập được dưới đây:
        ---
        {full_context}
        ---
        Hãy trả lời câu hỏi của người dùng một cách chính xác, đầy đủ và thân thiện.
        Nếu dữ liệu không có thông tin cụ thể, hãy thành thật trả lời là không rõ.
        Trả lời bằng tiếng việt, trừ khi khách yêu cầu bằng ngôn ngữ của họ
        
        Câu hỏi khách hàng: {query}
        """
        
        response = self.llm.invoke(prompt)
        return response.content
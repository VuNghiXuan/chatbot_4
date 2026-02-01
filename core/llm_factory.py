import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama # Đã cập nhật sang thư viện mới
from langchain_groq import ChatGroq

# Load các biến từ file .env
load_dotenv()

class LLMFactory:
    @staticmethod
    def get_llm(provider=None, model_name=None, api_key=None):
        # Lấy provider mặc định từ .env nếu không truyền vào
        provider = provider or os.getenv("DEFAULT_PROVIDER", "Ollama")
        
        if provider == "Gemini":
            m_name = model_name or os.getenv("GEMINI_MODEL")
            a_key = api_key or os.getenv("GOOGLE_API_KEY")
            return ChatGoogleGenerativeAI(model=m_name, google_api_key=a_key)
            
        elif provider == "Groq":
            m_name = model_name or os.getenv("GROQ_MODEL")
            a_key = api_key or os.getenv("GROQ_API_KEY")
            return ChatGroq(model_name=m_name, groq_api_key=a_key)
            
        elif provider == "Ollama":
            m_name = model_name or os.getenv("OLLAMA_MODEL")
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return ChatOllama(model=m_name, base_url=base_url)
            
        else:
            raise ValueError(f"Không hỗ trợ nhà cung cấp: {provider}")
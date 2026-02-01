"""
1. File: core/llm_factory.py (Lớp chọn LLMs)
Đây là Class mới để anh linh hoạt đổi "não" cho Bot.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq

class LLMFactory:
    @staticmethod
    def get_llm(provider, model_name, api_key=None):
        if provider == "Gemini":
            return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        elif provider == "Groq":
            return ChatGroq(model_name=model_name, groq_api_key=api_key)
        elif provider == "Ollama":
            return ChatOllama(model=model_name)
        else:
            raise ValueError(f"Không hỗ trợ nhà cung cấp: {provider}")
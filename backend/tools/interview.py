
import os
from langchain_groq import ChatGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def generate_interview_questions(role: str, seniority: str = "mid", count: int = 8) -> str:
    system_prompt = """You are an interview coach. Generate role-specific behavioral and technical questions.
For each question, add a short rubric: what a strong answer should include.
Group into categories if helpful. Keep it concise and skimmable.
"""
    user = f"Role: {role}\nSeniority: {seniority}\nCount: {count}\n\nGenerate questions with rubrics:"
    try:
        llm = ChatGroq(model_name=GROQ_MODEL, temperature=0.6, groq_api_key=GROQ_API_KEY)
        result = llm.invoke(f"{system_prompt}\n\n{user}")
        return getattr(result, "content", str(result)).strip()
    except Exception:
        return "I couldn't generate interview questions at the moment. Try again with role and desired count (e.g., 12)."

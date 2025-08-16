
import os
from langchain_groq import ChatGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def career_advice(prompt: str) -> str:
    system_prompt = """You are Alex Morgan, an experienced career coach and former recruiter.
Provide practical, specific, and encouraging guidance with examples and short action steps.
Conclude with one helpful follow-up question.
"""
    try:
        llm = ChatGroq(model_name=GROQ_MODEL, temperature=0.6, groq_api_key=GROQ_API_KEY)
        full = f"""{system_prompt}

User request:
{prompt}
"""
        result = llm.invoke(full)
        return getattr(result, "content", str(result)).strip()
    except Exception:
        return "I'm having trouble generating advice. Try again shortly, or share your target role and 3 companies you like."

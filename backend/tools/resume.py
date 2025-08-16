
import os
from langchain_groq import ChatGroq

# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

GROQ_API_KEY="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"
GROQ_MODEL="llama3-70b-8192"

def rewrite_resume(resume_text: str, target_role: str = "", target_company: str = "") -> str:
    """
    Rewrite resume content using LLM (if available), otherwise provide a simple heuristic rewrite.
    Returns the rewritten resume section (string).
    """
    system_prompt = """You are a resume rewriting assistant. Use strong, concise bullets with impact and metrics.
Follow best practices: action verbs, quantified results, ATS-friendly phrasing, and relevant keywords for the role.
Output a complete resume section rewrite and a short summary of changes."""
    prompt = f"Target role: {target_role or 'N/A'}\nTarget company: {target_company or 'N/A'}\n\nResume text to tailor:\n{resume_text}\n\nRewrite now:"

    try:
        if ChatGroq is None:
            # Basic fallback: attempt to produce concise bullets by simple heuristics
            lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
            bullets = []
            for i, l in enumerate(lines[:10]):
                bullets.append(f"- {l} (Improved bullet {i+1})")
            summary = "\nSummary: Converted to concise bullets and recommended adding metrics where possible."
            return "\n".join(bullets) + "\n\n" + summary
        llm = ChatGroq(model_name=GROQ_MODEL, temperature=0.5, groq_api_key=GROQ_API_KEY)
        result = llm.invoke(f"{system_prompt}\n\n{prompt}")
        return getattr(result, "content", str(result)).strip()
    except Exception as e:
        return "I couldn't rewrite the resume right now. Please try again, and include your target role for better tailoring. (" + str(e) + ")"
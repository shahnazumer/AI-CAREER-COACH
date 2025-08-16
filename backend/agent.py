
import os
from langchain.agents import tool
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from tools.career_advice import career_advice
from tools.resume import rewrite_resume
from tools.interview import generate_interview_questions
from tools.outreach import simulate_networking_outreach

from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

GROQ_API_KEY="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"
GROQ_MODEL="llama3-70b-8192"

# ----- Tools -----
@tool
def ask_career_coach(query: str) -> str:
    """
    Use for general career questions: job search strategy, skill gaps, negotiation,
    portfolio guidance, and targeted learning plans.
    """
    return career_advice(query)

@tool
def resume_rewrite_tool(resume_text: str, target_role: str = "", target_company: str = "") -> str:
    """
    Rewrite a resume for a target role/company. Provide 'resume_text' (paste) and optional
    'target_role' and 'target_company' for tailoring.
    """
    return rewrite_resume(resume_text=resume_text, target_role=target_role, target_company=target_company)

@tool
def interview_question_generator(role: str, seniority: str = "mid", count: int = 8) -> str:
    """
    Generate interview questions + what good answers include. 'role' required.
    """
    return generate_interview_questions(role=role, seniority=seniority, count=count)

@tool
def networking_outreach_tool(name: str = "Hiring Manager", to_email: str = "", role: str = "", company: str = "", platform: str = "Email") -> str:
    """
    Draft a short outreach message and SIMULATE sending (no external API). If 'to_email' is provided,
    include it in the status as a simulated recipient.
    """
    return simulate_networking_outreach(name=name, to_email=to_email, role=role, company=company, platform=platform)

tools = [ask_career_coach, resume_rewrite_tool, interview_question_generator, networking_outreach_tool]

# ----- LLM + Agent Graph (Groq) -----
llm = ChatGroq(model_name=GROQ_MODEL, temperature=0.2, groq_api_key=GROQ_API_KEY)
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI Career Coach helping users navigate roles, skills, resumes, interviews, networking, and job strategy.
You have access to these tools:

1. ask_career_coach — Use for general career questions and strategic guidance.
2. resume_rewrite_tool — Use when the user asks to rewrite or tailor a resume.
3. interview_question_generator — Use when the user asks for interview questions or prep.
4. networking_outreach_tool — Use when the user wants outreach messaging; sending is simulated.

Be concise, friendly, and practical. When drafting content, produce final usable text with bullet points where helpful.
If a location or specifics are truly essential, ask a brief clarifying question first.
End responses with one helpful follow-up question to keep momentum.
"""

def parse_response(stream):
    """Parses LangGraph stream to extract tool used and final message."""
    tool_called_name = "None"
    final_response = None

    for s in stream:
        tool_data = s.get("tools")
        if tool_data:
            tool_messages = tool_data.get("messages")
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, "name", tool_called_name)

        agent_data = s.get("agent")
        if agent_data:
            messages = agent_data.get("messages")
            if messages and isinstance(messages, list):
                for msg in messages:
                    if getattr(msg, "content", None):
                        final_response = msg.content
    return tool_called_name, final_response

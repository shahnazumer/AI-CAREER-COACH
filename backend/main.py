# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Import your AI agent system from agent.py (same directory)
from agent import graph, SYSTEM_PROMPT, parse_response

# Import tool functions (tools is a package folder inside backend/)
from tools.interview import generate_interview_questions
from tools.outreach import simulate_networking_outreach
from tools.resume import rewrite_resume
from tools.career_advice import career_advice

app = FastAPI(title="Career Coach AI Backend")

class Query(BaseModel):
    message: str

# ---------- Agent endpoint ----------
@app.post("/ask")
async def ask(query: Query):
    """
    Route to send an open message to the agent graph.
    We stream the graph response and parse it for which tool was called and final text.
    """
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    try:
        # graph.stream may be an iterator/generator that yields event dicts
        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)
    except Exception as e:
        # In production you'd log this. Return safe error to frontend.
        return {"response": "Agent processing failed: " + str(e), "tool_called": "None"}

    return {
        "response": final_response or "I couldn't generate a response right now.",
        "tool_called": tool_called_name,
    }

# ---------- Tool-specific endpoints ----------
class InterviewRequest(BaseModel):
    role: str
    seniority: str = "mid"
    count: int = 8

@app.post("/interview")
async def interview(req: InterviewRequest):
    return {"questions": generate_interview_questions(req.role, req.seniority, req.count)}

class OutreachRequest(BaseModel):
    name: str = "Hiring Manager"
    to_email: str = ""
    role: str = ""
    company: str = ""
    platform: str = "Email"

@app.post("/outreach")
async def outreach(req: OutreachRequest):
    return {"draft": simulate_networking_outreach(req.name, req.to_email, req.role, req.company, req.platform)}

class ResumeRequest(BaseModel):
    resume_text: str
    target_role: str = ""
    target_company: str = ""

@app.post("/resume")
async def resume(req: ResumeRequest):
    return {"rewritten": rewrite_resume(req.resume_text, req.target_role, req.target_company)}

class AdviceRequest(BaseModel):
    prompt: str

@app.post("/advice")
async def advice(req: AdviceRequest):
    return {"advice": career_advice(req.prompt)}

if __name__ == "__main__":
    # When running from backend directory: python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

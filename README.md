
# 🚀 AI Career Coach (Career Navigator)

An AI-powered **Career Coach** that helps with resumes, interviews, job search strategy, and networking.
Built with **LangGraph** (agent + tools), **LangChain** wrappers, and **Groq** (`llama3-70b-8192`).  
Networking outreach is **simulated** (no emails are sent).

## ✨ Features
- **Career coaching Q&A** — strategy, skills, salary negotiation, learning plans.
- **Resume rewrite** — paste your resume text + target role/company for tailored bullets.
- **Interview questions** — role-specific questions with mini rubrics.
- **Networking outreach** — drafts a message and simulates sending.

## 🧱 Architecture
- **Frontend**: `Streamlit` chat UI (`frontend.py`)
- **Backend**: `FastAPI` + **LangGraph** agent (`backend/agent.py`, `backend/main.py`)
- **Tools**:
  - `ask_career_coach` → Groq model responds as a recruiter/coach.
  - `resume_rewrite_tool` → Groq rewrites resume content for a target role.
  - `interview_question_generator` → Groq generates questions + rubrics.
  - `networking_outreach_tool` → drafts outreach (simulated send).

## 📂 Project Structure
```
career_coach_ai_groq_full/
├── frontend.py
├── backend/
│   ├── main.py
│   ├── agent.py
│   └── tools/
│       ├── career_advice.py
│       ├── resume.py
│       ├── interview.py
│       └── outreach.py
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
- Copy `.env` and set:
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama3-70b-8192
```

3. **Run the backend**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Run the frontend**
```bash
streamlit run frontend.py
```

5. **Open**: http://localhost:8501

## 💡 Example Prompts
- "Rewrite my resume for a Data Scientist role at Google."
- "What interview questions might I face for a Product Manager role?"
- "How do I negotiate salary as a mid-level marketing manager?"
- "Suggest a 30-day learning plan to transition into Cloud Engineering."
- "Draft a networking message to a recruiter at Microsoft."

## 🔁 Customize
- Change the model with `GROQ_MODEL` in `.env`.
- Update tone/behavior in `backend/tools/*.py` system prompts.
- Plug real event/job APIs if you want live data.

## 🔒 Notes
- Keep API keys in **.env** / host secrets (never commit).
- For production: add auth, rate limits, logging, and error monitoring.

## 📜 License
MIT — use and modify freely.

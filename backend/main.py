from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Initialize FastAPI app
app = FastAPI()

# 2. Security Configuration (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str

# 3. Define the Interface
@app.post("/analyze")
async def analyze_resume(request: AnalyzeRequest):
    score = 0
    
    return {
        "result": 
            f"Analysis Complete! Score: {score}/100",
            "missing_skills": ["AWS", "Docker"],
            "your_resume" : request.resume_text,
            "job_description" : request.jd_text
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import get_analysis_results

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
    analysis = get_analysis_results(request.resume_text, request.jd_text)
    
    score = analysis["match_score"]
    missing_skills = analysis["missing_skills"]
    
    return {
        "status": "success",
        "match_score": f"{score}%",
        "missing_skills": missing_skills,
        "details": {
            "resume_length": len(request.resume_text),
            "jd_length": len(request.jd_text)
        }
    }
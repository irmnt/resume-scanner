from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import pdfplumber
import io
import logging
import warnings
from fastapi.middleware.cors import CORSMiddleware
from utils import get_analysis_results

# Suppress PDF font warnings
warnings.filterwarnings("ignore", message=".*FontBBox.*")
logging.getLogger("pdfminer").setLevel(logging.ERROR)

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

async def extract_text_from_pdf(file: UploadFile, file_type_name: str) -> str:
    """Helper function to extract text from PDF files."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail=f"Only PDF files are supported for {file_type_name}.")
    
    extracted_text = ""
    try:
        file_bytes = await file.read()
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail=f"Could not extract text from the {file_type_name} PDF. Please ensure it's a valid document.")
        
        return extracted_text
    
    except HTTPException:
        # Preserve HTTP errors raised deliberately for invalid inputs
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the {file_type_name} PDF: {str(e)}")

@app.post("/analyze")
async def analyze_documents(
    resume_text: str = Form(None),
    jd_text: str = Form(None),
    resume_file: UploadFile = File(None),
    jd_file: UploadFile = File(None)
):
    # 1. resolve Resume Data
    final_resume_text = ""
    if resume_file:
        final_resume_text = await extract_text_from_pdf(resume_file, "Resume")
    elif resume_text:
        final_resume_text = resume_text
    else:
        raise HTTPException(status_code=400, detail="Please provide a Resume either as text or as a PDF file.")
    
    # 2. Resolve JD Data
    final_jd_text = ""
    if jd_file:
        final_jd_text = await extract_text_from_pdf(jd_file, "Job Description")
    elif jd_text:
        final_jd_text = jd_text
    else:
        raise HTTPException(status_code=400, detail="Please provide a Job Description either as text or as a PDF file.")
        
    try:
        analysis = get_analysis_results(final_resume_text, final_jd_text)
        
        return {
            "status": "success",
            "match_score": analysis["match_score"],
            "missing_skills": analysis["missing_skills"],
            "experience_analysis": analysis["experience_analysis"],
            "education_analysis": analysis["education_analysis"],
            "details": {
                "resume_skills_found": analysis["details"]["resume_skills_found"],
                "jd_skills_required": analysis["details"]["jd_skills_required"],
                "resume_education": analysis["details"]["resume_education"],
                "jd_education_required": analysis["details"]["jd_education_required"],
            }
        }    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while analyzing the documents: {str(e)}")
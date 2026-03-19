import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Add it to backend/.env or export it as an environment variable.")

# 2. configure the API
genai.configure(api_key=GEMINI_API_KEY)

def get_analysis_results(r_text: str, jd_text: str):
    """
    Sends the Resume and JD to Google's gemini LLM and
    requests a strictly formatted JSON response.
    """
    
    # 2. Initialize the model
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # 3. Craft the "System prompt" to force the exact jsON structure
    prompt = f"""
    You are an expert Applicant Tracking System algorithm.
    Strictly evaluate the candidate's Resume against the Job Description.

    Important: focus on actual candidate work experience evidence.
    - "experience_analysis" must be derived solely from resume project/job bullets (role/title, company, dates, responsibilities, technical actions, project context, and impact).
    - Do NOT include raw JD requirement text inside "experience_analysis".
    - OpenStack requirements should be evaluated in a separate optional section (e.g. "requirement_analysis" or "skills_analysis").
    - If you choose to include requirement-level gaps, keep them distinct from experience narrative.

    Resume Text: 
    {r_text}
    Job Description Text: 
    {jd_text}

    Analyze the candidate's work experience and skill coverage.
    For `experience_analysis`, include only requirements or statements that contain the word "experience" (or clearly indicate hands-on professional role/project usage); exclude purely hard-skill checklist items.
    For other JD lines, use `requirement_analysis` and/or `skills_analysis`.
    Respond ONLY with a valid JSON object matching the exact schema below.

    Do not include any other conversational text or markdown formatting blocks.

    {{
        "match_score": "A string representing the overall match percentage from 0.0% to 100.0%. Weight skills (50%), experience (30%), and education (20%).",
        "missing_skills": ["List", "of", "missing", "hard", "technical", "skills"],
        "experience_analysis": [
            {{
                "requirement": "Specific experience requirement from JD",
                "status": "Must be exactly one of: 'Qualified', 'Partially Matched Domain', 'Less Qualified (Years)', or 'Unmatched Domain'",
                "details": "A brief 1-sentence explanation of why this status was chosen"
            }}
        ],
        "skills_analysis": [
            {{
                "skill": "Specific skill or technology",
                "status": "Must be exactly one of: 'Matched', 'Partially Matched', or 'Unmatched'",
                "details": "A brief 1-sentence explanation of why this status was chosen"
            }}
        ],
        "education_analysis": [
            {{
                "requirement": "Specific education requirement from JD",
                "status": "Must be exactly one of: 'Matched', 'Partially Matched', or 'Unmatched'",
                "details": "A brief 1-sentence explanation of the candidate's education compared to the requirement"
            }}
        ],
        "details": {{
            "resume_skills_found": ["List", "of", "skills", "found", "in", "resume"],
            "jd_skills_required": ["List", "of", "skills", "requested", "in", "JD"],
            "resume_education": ["List", "of", "degrees/certs", "in", "resume"],
            "jd_education_required": ["List", "of", "degrees/certs", "requested", "in", "JD"]
        }}
    }}
    """
    
    try:
        print("--- Sending dta to Gemini API...")
        # 4. Ask the LLM to generate the JSON payload
        response = model.generate_content(prompt)
        
        # 5. Clea the response
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3]
            
        # 6. Convert the LLM's string into a Python Dictionary
        parsed_json = json.loads(raw_text)
        print("--- Successfully generated AI response!")
        return parsed_json

    except Exception as e:
        print(f"--- ERROR Calling LLM: {str(e)}")
        # Fallback to prevent the server/frontend from crashing
        return {
            "match_score": "0.0%",
            "missing_skills": ["API Connection Error"],
            "experience_analysis": [],
            "education_analysis": [],
            "details": {
                "resume_skills_found": [],
                "jd_skills_required": [],
                "resume_education": [],
                "jd_education_required": []
            }
        }

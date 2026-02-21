import spacy
from spacy.pipeline import EntityRuler
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# 1. Load the Model
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Downloading 'en_core_web_md' model...")
    from spacy.cli import download
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")
    

# 2. Configuration: The Knowledge Base
def setup_nlp_pipeline(nlp):
    # 1. Safely check if the ruler exists
    if "entity_ruler" not in nlp.pipe_names:
        # Create it if it is missing
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    else:
        # Grab it if it already exists (due to Uvicorn reload)
        ruler = nlp.get_pipe("entity_ruler")
        # Clear old patterns so they don't stack up infinitely
        ruler.clear()
    
    # 2. Add your patterns
    patterns = [
        {"label": "SKILL", "pattern": [{"LOWER": "python"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "java"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "javascript"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "typescript"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "sql"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "c++"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "c#"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "go"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "react"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "vue"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "angular"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "fastapi"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "django"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "flask"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "spring"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "aws"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "azure"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "gcp"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "docker"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "kubernetes"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "terraform"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "jenkins"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "git"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "machine"}, {"LOWER": "learning"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "rest"}, {"LOWER": "api"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "agile"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "ci"}, {"LOWER": "/" }, {"LOWER": "cd"}]},
    ]
    
    ruler.add_patterns(patterns)
    return nlp

# Initialize Pipeline immediately
nlp = setup_nlp_pipeline(nlp)

# 3. INTERNAL HELPER (The Shared Logic)
def _extract_skills(doc):
    """
    Helper function to extract skills from any spaCy Doc.
    Used by both JD and Resume parsers to avoid duplicating code.
    """
    # Use a set to avoid duplicates (e.g., finding "Python" twice)
    return set([ent.text for ent in doc.ents if ent.label_ == "SKILL"])

# 4. PUBLIC FUNCTION 1: JD Sanitization
def sanitize_jd(text: str):
    """
    Processes the Job Description.
    PLACEHOLDER FOR FUTURE UPGRADE: 
    - Add logic here to remove "Benefits" or "Legal" sections.
    - Extract "Years of Experience" requirements.
    """
    doc = nlp(text)
    skills = _extract_skills(doc)
    
    return {
        "type": "JD",
        "skills": skills,
        "doc": doc
    }

# 5. PUBLIC FUNCTION 2: Resume Sanitization
def sanitize_resume(text: str):
    """
    Processes the Resume.
    PLACEHOLDER FOR FUTURE UPGRADE: 
    - Add logic here to anonymize the candidate (remove Name/Email).
    """
    doc = nlp(text)
    skills = _extract_skills(doc)
    
    return {
        "type": "RESUME",
        "skills": skills,
        "doc": doc
    }
    

# 6. THE ORCHESTRATOR (Called by API)
def get_analysis_results(resume_text: str, jd_text: str):
    # Step 1: Process independently using specialized functions
    resume_data = sanitize_resume(resume_text)
    jd_data = sanitize_jd(jd_text)
    
    # Step 2: Compare Skills (Hard Match)
    resume_skills = resume_data["skills"]
    jd_skills = jd_data["skills"]
    
    # Find what is in JD but NOT in Resume
    missing_skills = list(jd_skills - resume_skills)
    
    # Step 3: Compare Semantics (Soft Match)
    # .similarity() returns a float between 0.0 and 1.0
    semantic_match = resume_data["doc"].similarity(jd_data["doc"])
    
    # Step 4: Formatting
    return {
        "match_score": f"{round(semantic_match * 100, 1)}",
        "missing_skills": missing_skills,
        "details": {
            "resume_skills_found": list(resume_skills),
            "jd_skills_required": list(jd_skills)
        }
    }

# Test Block
if __name__ == "__main__":
    print("--- Running Architecture Test ---")
    r_text = "I am a Python developer with experience in AWS and Fastapi."
    j_text = "We are looking for a Python developer with AWS, Docker, and Kubernetes skills."
    
    result = get_analysis_results(r_text, j_text)
    print(f"Match Score: {result['match_score']}")
    print(f"Missing Skills: {result['missing_skills']}")

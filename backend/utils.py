import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher
from spacy.util import filter_spans
import warnings
import logging

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
logging.getLogger("pdfminer").setLevel(logging.ERROR)

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
        # programming languages
        {"label": "SKILL", "pattern": [{"LOWER": "python"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "java"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "javascript"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "typescript"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "sql"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "c++"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "c#"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "go"}]},
        # frameworks and tools
        {"label": "SKILL", "pattern": [{"LOWER": "react"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "vue"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "angular"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "fastapi"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "django"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "flask"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "spring"}]},
        # data tools
        {"label": "SKILL", "pattern": [{"LOWER": "postgresql"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "mysql"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "rds"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "vectore db"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "graph db"}]},
        # cloud platforms
        {"label": "SKILL", "pattern": [{"LOWER": "aws"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "azure"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "gcp"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "docker"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "kubernetes"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "terraform"}]},
        # ci/cd and other tools
        {"label": "SKILL", "pattern": [{"LOWER": "jenkins"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "git"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "machine"}, {"LOWER": "learning"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "rest"}, {"LOWER": "api"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "agile"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "ci"}, {"LOWER": "/" }, {"LOWER": "cd"}]},
        # AI/ML specific
        {"label": "SKILL", "pattern": [{"LOWER": "ai"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "claude code"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "copilot"}]},
        {"label": "SKILL", "pattern": [{"LOWER": "cursor"}]},
        
        # EDUCATION: Degree Types
        {"label": "EDUCATION", "pattern": [{"LOWER": "bachelor's"}, {"LOWER": "degree"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "bachelor"}, {"LOWER": "of"}, {"LOWER": "science"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "bachelor"}, {"LOWER": "of"}, {"LOWER": "engineering"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "master's"}, {"LOWER": "degree"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "master"}, {"LOWER": "of"}, {"LOWER": "science"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "master"}, {"LOWER": "of"}, {"LOWER": "business"}, {"LOWER": "administration"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "phd"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "doctorate"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "mba"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "b.s."}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "b.a."}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "b.e."}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "b.tech"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "m.s."}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "m.a."}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "m.tech"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "associate's"}, {"LOWER": "degree"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "associate"}, {"LOWER": "degree"}]},
        # EDUCATION: Fields of Study
        {"label": "EDUCATION", "pattern": [{"LOWER": "computer"}, {"LOWER": "science"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "computer"}, {"LOWER": "engineering"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "information"}, {"LOWER": "technology"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "software"}, {"LOWER": "engineering"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "data"}, {"LOWER": "science"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "electrical"}, {"LOWER": "engineering"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "mechanical"}, {"LOWER": "engineering"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "management"}, {"LOWER": "information"}, {"LOWER": "systems"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "business"}, {"LOWER": "administration"}]},
        # EDUCATION: Internship-Specific (Ongoing Education)
        {"label": "EDUCATION", "pattern": [{"LOWER": "currently"}, {"LOWER": "pursuing"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "currently"}, {"LOWER": "enrolled"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "pursuing"}, {"LOWER": "degree"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "enrolled"}, {"LOWER": "in"}]},
        # EDUCATION: Year in School
        {"label": "EDUCATION", "pattern": [{"LOWER": "1st"}, {"LOWER": "year"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "2nd"}, {"LOWER": "year"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "3rd"}, {"LOWER": "year"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "4th"}, {"LOWER": "year"}]},
        # EDUCATION: Expected Graduation
        {"label": "EDUCATION", "pattern": [{"LOWER": "expected"}, {"LOWER": "graduation"}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "graduation"}, {"TEXT": ":"}, {"LIKE_NUM": True}]},
        {"label": "EDUCATION", "pattern": [{"LOWER": "grad"}, {"TEXT": ":"}, {"LIKE_NUM": True}]},
        
    ]
    ruler.add_patterns(patterns)
    
    # 3. Setup Matcher for Experience Extraction
    matcher = Matcher(nlp.vocab)
    exp_pattern = [
        {"LIKE_NUM": True}, 
        {"TEXT": "+", "OP": "?"}, # To capture "5+" years
        {"LOWER": {"IN": ["year", "years", "yrs"]}},
        {"LOWER": "of", "OP": "?"},
        {"LOWER": "experience", "OP": "?"},
        {"LOWER": "in", "OP": "?"},
        {"POS": "DET", "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "PUNCT", "VERB", "ADP", "CCONJ"]}, "OP": "+"}
    ]
    matcher.add("EXPERIENCE", [exp_pattern])
    
    return nlp, matcher

# Initialize Pipeline immediately
nlp, matcher = setup_nlp_pipeline(nlp)

# 3. INTERNAL HELPER (The Shared Logic)
def _extract_skills(doc):
    """
    Helper function to extract skills from any spaCy Doc.
    Used by both JD and Resume parsers to avoid duplicating code.
    """
    # Use a set to avoid duplicates (e.g., finding "Python" twice)
    return set([ent.text for ent in doc.ents if ent.label_ == "SKILL"])

def _extract_experience(doc):
    """
    Helper function to extract years of experience from any spaCy Doc.
    """
    matches = matcher(doc)
    
    spans = [doc[start:end] for match_id, start, end in matches]
    filtered_spans = filter_spans(spans)
    
    return [span.text for span in filtered_spans]

def _extract_education(doc):
    """
    Helper function to extract education qualifications from any spaCy Doc.
    Returns a list of unique education entities found.
    """
    return list(set([ent.text for ent in doc.ents if ent.label_ == "EDUCATION"]))

def parse_experience_string(exp_string: str):
    """
    Turns '5 years in Software Engineering' into structured data:
    {'years': 5.0, 'domain': 'Software Engineering'}
    """
    doc = nlp(exp_string)
    years = 0
    
    # Extract number
    numbers = [token.text for token in doc if token.like_num]
    if numbers:
        try:
            years = float(numbers[0])
        except ValueError:
            pass 

    # Extract domain (everything after "in" or "of")
    domain_text = "General"
    for token in doc:
        if token.text.lower() in ["in", "of"]:
            domain_text = doc[token.i + 1 :].text
            break
            
    return {"years": years, "domain": domain_text, "doc": nlp(domain_text)}

def evaluate_candidate_experience(resume_exp_list, jd_exp_list):
    """
    Compares the candidate's experience against JD requirements.
    """
    evaluations = []
    
    # If JD doesn't ask for experience, skip logic
    if not jd_exp_list:
        return []

    for jd_item in jd_exp_list:
        jd_parsed = parse_experience_string(jd_item)
        best_match = None
        highest_score = 0
        
        # Compare against every experience listed in Resume
        for res_item in resume_exp_list:
            res_parsed = parse_experience_string(res_item)
            
            # Check Similarity of Domain (e.g. "Software" vs "AI")
            similarity = jd_parsed["doc"].similarity(res_parsed["doc"])
            
            if similarity > highest_score:
                highest_score = similarity
                best_match = res_parsed
        
        # JUDGMENT LOGIC
        status = "Not Found"
        details = "No matching experience found."
        
        if best_match:
            # Rule 1: Totally different field?
            if highest_score < 0.5:
                status = "Unmatched Domain"
                details = f"Found {best_match['domain']} (Low similarity)"
            # Rule 2: Similar field, but not close enough?
            elif highest_score < 0.75:
                status = "Partially Matched Domain"
                details = f"Found {best_match['domain']} (Moderate similarity)"
            # Rule 3: Same field, but not enough years?
            elif best_match["years"] < jd_parsed["years"]:
                status = "Less Qualified (Years)"
                details = f"Found {best_match['years']} years (Required: {jd_parsed['years']})"
            # Rule 4: Sufficient?
            else:
                status = "Qualified"
                details = f"Found {best_match['years']} years in {best_match['domain']}"
                
            evaluations.append({
                "requirement": jd_item,
                "status": status,
                "details": details
            })
            
    return evaluations

def evaluate_candidate_education(resume_edu_list, jd_edu_list):
    """
    Compares the candidate's education against JD requirements.
    """
    evaluations = []
    
    # If JD doesn't specify education requirements, skip
    if not jd_edu_list:
        return []
    
    for jd_requirement in jd_edu_list:
        jd_lower = jd_requirement.lower()
        
        # Check for exact or similar matches
        found_match = None
        highest_similarity = 0
        
        for r_edu in resume_edu_list:
            r_lower = r_edu.lower()
            
            # Create spaCy docs for similarity comparison
            jd_doc = nlp(jd_lower)
            res_doc = nlp(r_lower)
            similarity = jd_doc.similarity(res_doc)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                found_match = r_edu
        
        # JUDGMENT LOGIC
        status = "Not Found"
        details = "No matching education found."
        
        if found_match:
            if highest_similarity >= 0.8:
                status = "Matched"
                details = f"Found: {found_match}"
            elif highest_similarity >= 0.6:
                status = "Partially Matched"
                details = f"Found: {found_match} (Similar)"
            else:
                status = "Unmatched"
                details = f"Found: {found_match} (Different qualification)"
        
        evaluations.append({
            "requirement": jd_requirement,
            "status": status,
            "details": details
        })
    
    return evaluations

# 4. PUBLIC FUNCTION 1: JD Sanitization
def sanitize_jd(text: str):
    """
    Processes the Job Description.
    PLACEHOLDER FOR FUTURE UPGRADE: 
    - Add logic here to remove "Benefits" or "Legal" sections.
    - Extract "Years of Experience" requirements.
    """
    doc = nlp(text)
    
    return {
        "type": "JD",
        "skills": _extract_skills(doc),
        "experience": _extract_experience(doc),
        "education": _extract_education(doc),
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
    
    return {
        "type": "RESUME",
        "skills": _extract_skills(doc),
        "experience": _extract_experience(doc),
        "education": _extract_education(doc),
        "doc": doc
    }
    

# 6. THE ORCHESTRATOR (Called by API)
def get_analysis_results(resume_text: str, jd_text: str):
    # Step 1: Process independently using specialized functions
    resume_data = sanitize_resume(resume_text)
    jd_data = sanitize_jd(jd_text)
    
    # Step 2: Compare Skills (Hard Match)
    jd_skills = jd_data["skills"]
    resume_skills = resume_data["skills"]
    
    jd_lower = {skill.lower() for skill in jd_skills}
    resume_lower = {skill.lower() for skill in resume_skills}
    missing_lower = jd_lower - resume_lower
    missing_skills = [skill for skill in jd_skills if skill.lower() in missing_lower]
    
    # Step 3: Compare Experience
    experience_analysis = evaluate_candidate_experience(
        resume_data["experience"],
        jd_data["experience"]
    )
    
    # Step 4: Compare Education
    education_analysis = evaluate_candidate_education(
        resume_data["education"],
        jd_data["education"]
    )
    
    # Step 5: Calculate ATS Match Score
    total_jd_skills = len(jd_lower)
    
    if total_jd_skills > 0:
        skill_matched = total_jd_skills - len(missing_skills)
        skill_score = (skill_matched / total_jd_skills) * 100
    else:
        skill_score = 100.0
    
    
    exp_score = 100.0
    if experience_analysis:
        points_per_exp = 100.0 / len(experience_analysis)
        
        for exp in experience_analysis:
            if exp["status"] == "Unmatched Domain":
                exp_score -= points_per_exp
            elif exp["status"] == "Less Qualified (Years)":
                exp_score -= (points_per_exp * 0.5)
    
    edu_score = 100.0
    if education_analysis:
        points_per_edu = 100.0 / len(education_analysis)
        
        for edu in education_analysis:
            if edu["status"] == "Unmatched":
                edu_score -= points_per_edu
            elif edu["status"] == "Partially Matched":
                edu_score -= (points_per_edu * 0.5)
    
    SKILL_WEIGHT = 0.50
    EXP_WEIGHT = 0.30
    EDU_WEIGHT = 0.20
    
    final_score = (skill_score * SKILL_WEIGHT) + (exp_score * EXP_WEIGHT) + (edu_score * EDU_WEIGHT)
    final_score = max(0.0, final_score)
    
    # Step 6: Formatting
    return {
        "match_score": f"{round(final_score, 1)}%",
        "missing_skills": missing_skills,
        "experience_analysis": experience_analysis,
        "education_analysis": education_analysis,
        "details": {
            "resume_skills_found": list(resume_skills),
            "jd_skills_required": list(jd_skills),
            "resume_education": resume_data["education"],
            "jd_education_required": jd_data["education"],
        }
    }

# Test Block
if __name__ == "__main__":
    print("--- Testing Experience Logic ---")
    r_text = "I have 2 years of experience in Software Engineering and 1 year in React."
    j_text = "Required: 5 years of experience in Software Engineering."
    
    result = get_analysis_results(r_text, j_text)
    print("Experience Analysis:", result["experience_analysis"])

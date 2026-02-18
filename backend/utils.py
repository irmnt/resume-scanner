import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load the small English model
nlp = spacy.load("en_core_web_md")

def sanitize_text(text: str):
    """
    Cleans text by removing punctuation, stop words, and converting to lemmas.s
    """
    # 1. process the text with spacy
    doc = nlp(text.lower())
    
    # 2. Filter out stop words and punctuation, and lemmatize the tokens
    clean_tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ] 
    
    return " ".join(clean_tokens)

def get_analysis_results(resume_text: str, jd_text: str):
    # 1. Sanitize the inputs
    clean_resume = sanitize_text(resume_text)
    clean_jd = sanitize_text(jd_text)
    
    # 2. Vectorization (Turning text into numbers)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([clean_resume, clean_jd])
    
    # 3. Calculat Cosine Similarity
    similarlity_matrix = cosine_similarity(vectors)
    # Get the similarity score between resume and JD
    match_percentage = round(similarlity_matrix[0][1] * 100, 2) 
    
    # 4. find Missing Keywords
    resume_words = set(clean_resume.split())
    jd_words = set(clean_jd.split())
    missing_skills = list(jd_words - resume_words)
    
    return {
        "match_score": match_percentage,
        "missing_skills": missing_skills[:10]
    }


if __name__ == "__main__":
    test_resume = "Software Engineer with experience in Python, API development, and React."
    test_jd = "Looking for a Software Engineer skilled in Python, APIs, and AWS Cloud."
    
    results = get_analysis_results(test_resume, test_jd)
    
    print("--- Analysis Results ---")
    print(f"Match Score: {results['match_score']}%")
    print(f"Missing Skills: {results['missing_skills']}")
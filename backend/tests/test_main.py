import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app  # This assumes your FastAPI instance is in a file named main.py

# Test categories in this file:
# 1) Happy path behavior: analyze endpoint with valid resume/jd input returns 200 + structured response.
# 2) Input validation failures: resume or jd missing, invalid file type, empty PDF extraction → 400.
# 3) Internal error handling: get_analysis_results exception -> 500.
# 4) File upload workflow: PDF file upload path with mocked PDF extraction and analysis results.

# 1. Initialize the "Invisible Browser"
# This allows us to send HTTP requests to our app without actually starting the Uvicorn server!
client = TestClient(app)

# 2. The Mocking Stunt Double
# We do NOT want to call Google Gemini during a test. It costs money and time.
# @patch intercepts the import of 'get_analysis_results' inside your main.py file.
# Note: If your import looks like 'import utils', you would patch "main.utils.get_analysis_results" instead.
@patch("main.get_analysis_results") 

# Category: Happy path behavior
# Execute this to verify endpoint returns 200 with formatted analysis structure
# and propagates analysis data from get_analysis_results.
def test_analyze_endpoint_success(mock_get_analysis):
    
    # 3. Create the Fake AI Response
    # We tell our stunt double: "When you are called, just return this fake dictionary immediately."
    mock_get_analysis.return_value = {
        "match_score": "85.0%",
        "missing_skills": ["Docker", "Kubernetes"],
        "experience_analysis": [],
        "education_analysis": [],
        "details": {
            "resume_skills_found": ["Python"],
            "jd_skills_required": ["Python", "Docker", "Kubernetes"],
            "resume_education": ["B.Sc Computer Science"],
            "jd_education_required": ["Bachelor's degree"]
        }
    }

    # 4. Prepare the Fake User Input
    # This is exactly what your React frontend sends when someone clicks "Analyze"
    payload = {
        "resume_text": "I am a backend developer with 3 years of Python experience.",
        "jd_text": "Looking for a backend developer who knows Python, Docker, and Kubernetes."
    }

    # 5. Act: Send the POST request to your endpoint
    response = client.post("/analyze", data=payload)

    # 6. ASSERTIONS: The QA Checklist
    
    # Checklist Item 1: Did the server respond successfully? (Status 200 OK)
    assert response.status_code == 200
    
    # Checklist Item 2: Did the server return our fake data correctly formatted?
    response_data = response.json()
    
    # We assert that the match score made it through to the final response
    assert response_data["match_score"] == "85.0%"
    
    # We assert that 'Docker' was successfully identified in the missing skills list
    assert "Docker" in response_data["missing_skills"]


# Category: Input validation failures
# Execute these to verify missing required input returns 400 with clear error message.
def test_analyze_endpoint_missing_resume_text_and_file_returns_400():
    payload = {"jd_text": "Looking for X"}
    response = client.post("/analyze", data=payload)
    assert response.status_code == 400
    assert "Please provide a Resume" in response.json()["detail"]


def test_analyze_endpoint_missing_jd_text_and_file_returns_400():
    payload = {"resume_text": "I know Python"}
    response = client.post("/analyze", data=payload)
    assert response.status_code == 400
    assert "Please provide a Job Description" in response.json()["detail"]


# Category: Internal error handling
# Execute this to verify an internal exception from analysis service results in 500.
@patch("main.get_analysis_results")
def test_analyze_endpoint_get_analysis_results_raises_returns_500(mock_get_analysis):
    mock_get_analysis.side_effect = Exception("fake analysis error")

    payload = {
        "resume_text": "I am a backend developer with 3 years of Python experience.",
        "jd_text": "Looking for a backend developer who knows Python, Docker, and Kubernetes."
    }

    response = client.post("/analyze", data=payload)
    assert response.status_code == 500
    assert "An error occurred while analyzing the documents" in response.json()["detail"]


# Category: File upload and PDF handling
# Execute these to validate PDF type checks and text extraction behavior.
def test_analyze_endpoint_invalid_resume_file_type_returns_400():
    files = {"resume_file": ("resume.txt", b"notapdf", "text/plain")}
    data = {"jd_text": "Looking for X"}
    response = client.post("/analyze", data=data, files=files)

    assert response.status_code == 400
    assert "Only PDF files are supported for Resume" in response.json()["detail"]


@patch("main.pdfplumber.open")
def test_analyze_endpoint_resume_pdf_no_text_returns_400(mock_pdfplumber_open):
    class DummyPage:
        def extract_text(self):
            return None

    class DummyPDF:
        pages = [DummyPage()]

    mock_pdfplumber_open.return_value.__enter__.return_value = DummyPDF()

    files = {"resume_file": ("resume.pdf", b"%PDF-1.4 dummy", "application/pdf")}
    data = {"jd_text": "Some JD"}
    response = client.post("/analyze", data=data, files=files)

    assert response.status_code == 400
    assert "Could not extract text from the Resume PDF" in response.json()["detail"]


# Category: File upload and PDF handling (continued)
# Execute this to verify that uploading valid PDFs produces success via mocked PDF extraction + analysis.
@patch("main.get_analysis_results")
@patch("main.extract_text_from_pdf", new_callable=AsyncMock)
def test_analyze_endpoint_file_upload_success(mock_extract_text_from_pdf, mock_get_analysis):
    mock_extract_text_from_pdf.side_effect = ["Candidate resume text", "JD text"]
    mock_get_analysis.return_value = {
        "match_score": "88.0%",
        "missing_skills": ["Kubernetes"],
        "experience_analysis": [],
        "education_analysis": [],
        "details": {
            "resume_skills_found": ["Python"],
            "jd_skills_required": ["Python", "Docker"],
            "resume_education": ["B.Sc"],
            "jd_education_required": ["Bachelor's"]
        }
    }

    files = {
        "resume_file": ("resume.pdf", b"%PDF-1.4 dummy", "application/pdf"),
        "jd_file": ("jd.pdf", b"%PDF-1.4 dummy", "application/pdf")
    }
    response = client.post("/analyze", data={}, files=files)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["match_score"] == "88.0%"
    assert "Kubernetes" in body["missing_skills"]
    assert body["details"]["resume_skills_found"] == ["Python"]


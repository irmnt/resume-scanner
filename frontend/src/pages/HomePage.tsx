import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
    // State of the resume text and job description text
    const [resumeText, setResumeText] = useState<string>('');
    const [jdText, setJdText] = useState<string>('');
    const navigate = useNavigate();

    /* API call */
    const handleScan = async () => {
        try {
            // 1. Point to the running backend URL
            const response = await fetch('http://127.0.0.1:8001/analyze',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },

                    // 2. The keys MUST match the Pydantic model in the backend
                    body: JSON.stringify({
                        resume_text: resumeText,
                        jd_text: jdText
                    }),
                });

            const data = await response.json();

            // 3. Navigate the response data to the ResultPage
            navigate('/result', { state: { analysisData: data } });

        } catch (error) {
            console.error('Error:', error);
            alert("Error: Could not connect to scanner backend.");
        }
    };


    return (
        <>
            <h1>RESUME SCANNER</h1>
            <div className="resume-input">

                {/* Resume Input */}
                <h4>Input your resume here</h4>
                <textarea
                    id="resume-text"
                    rows={10}       // Sets initial height (in lines of text)
                    placeholder="Copy and paste your resume text here..."
                    className="resizable-box"

                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                />
            </div>

            {/* Job Description Input */}
            <div className="jd-input">
                <h4>Input the job description here</h4>
                <textarea
                    id="jd-text"
                    rows={10}       // Sets initial height (in lines of text)
                    placeholder="Copy and paste the job description here..."
                    className="resizable-box"
                    value={jdText}
                    onChange={(e) => setJdText(e.target.value)}
                />

                {/* The Button Trigger*/}
            </div>
            <div className="buttons">
                <button onClick={handleScan}>Analyze</button>
            </div>
        </>
    );
}
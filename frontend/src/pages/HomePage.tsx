import { use, useState } from "react";
import { resume } from "react-dom/server";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
    // State for Text Inputs
    const [resumeText, setResumeText] = useState<string>('');
    const [jdText, setJdText] = useState<string>('');
    // State for File Inputs
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [jdFile, setJDFile] = useState<File | null>(null);
    // State for inpute Modes
    const [resumeMode, setResumeMode] = useState<'text' | 'pdf'>('text');
    const [jdMode, setJdMode] = useState<'text' | 'pdf'>('text');
    // State for UX
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const navigate = useNavigate();

    /* API call */
    const handleScan = async () => {
        // 1. Basic validation
        if (!resumeText.trim() && !resumeFile) {
            return alert("Please provide either resume text or upload a resume file.");
        }
        if (!jdText.trim() && !jdFile) {
            return alert("Please provide either job description text or upload a JD file.");
        }

        setIsLoading(true);

        try {
            // 2. Build the formData object
            const formData = new FormData();

            // Only append the data if the user actually provided it
            if (resumeMode === 'text' && resumeText.trim()) {
                formData.append('resume_text', resumeText);

            } else if (resumeMode === 'pdf' && resumeFile) {
                formData.append('resume_file', resumeFile);

            } else {
                return alert("Please provide your resume");
            }

            if (jdMode === 'text' && jdText.trim()) {
                formData.append('jd_text', jdText);
            } else if (jdMode === 'pdf' && jdFile) {
                formData.append('jd_file', jdFile);
            } else {
                return alert("Please provide the job description");
            }

            // 3. Point to the running backend URL
            const response = await fetch('http://127.0.0.1:8001/analyze',
                {
                    method: 'POST',
                    body: formData,
                });

            if (!response.ok) {
                // Try to catch the specific error message from the backend
                const errorData = await response.json();
                throw new Error(errorData.detail || "Server responded with an error.");
            }

            // 4. Navigate the response data to the ResultPage
            const data = await response.json();
            navigate('/result', { state: { analysisData: data } });

        } catch (error) {
            console.error('Error:', error);
            alert("Error: Could not connect to scanner backend.");
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <>
            <h1>RESUME SCANNER</h1>

            <div className="input-container">
                {/* --- RESUME SECTION --- */}
                <div className="resume-input">
                    <h2>1. your resume</h2>

                    {/* Toggle Buttons */}
                    <div className="toggle-group">
                        <button
                            className={resumeMode === 'text' ? 'active-toggle' : ''}
                            onClick={() => setResumeMode('text')}
                        >
                            Paste Text
                        </button>
                        <button
                            className={resumeMode === 'pdf' ? 'active-toggle' : ''}
                            onClick={() => setResumeMode('pdf')}
                        >
                            Upload PDF
                        </button>
                    </div>

                    {/* Conditional Rendering */}
                    {resumeMode === 'text' ? (
                        <textarea
                            id="resume-text"
                            rows={10}
                            placeholder="Copy and paste your resume text here..."
                            className="resizable-box"
                            value={resumeText}
                            onChange={(e) => setResumeText(e.target.value)}
                        />
                    ) : (
                        <div className="file-upload-box">
                            <input
                                type="file"
                                accept=".pdf"
                                onChange={(e) => setResumeFile(e.target.files ? e.target.files[0] : null)}
                            />
                        </div>
                    )}
                </div>

                {/* --- JOB DESCRIPTION SECTION --- */}
                <div className="jd-input">
                    <h2>2. job description</h2>

                    {/* Toggle Buttons */}
                    <div className="toggle-group">
                        <button
                            className={jdMode === 'text' ? 'active-toggle' : ''}
                            onClick={() => setJdMode('text')}
                        >
                            Paste Text
                        </button>
                        <button
                            className={jdMode === 'pdf' ? 'active-toggle' : ''}
                            onClick={() => setJdMode('pdf')}
                        >
                            Upload PDF
                        </button>
                    </div>

                    {/* Conditional Rendering */}
                    {jdMode === 'text' ? (
                        <textarea
                            id="jd-text"
                            rows={10}
                            placeholder="Copy and paste the job description here..."
                            className="resizable-box"
                            value={jdText}
                            onChange={(e) => setJdText(e.target.value)}
                        />
                    ) : (
                        <div className="file-upload-box">
                            <input
                                type="file"
                                accept=".pdf"
                                onChange={(e) => setJDFile(e.target.files ? e.target.files[0] : null)}
                            />
                        </div>
                    )}
                </div>
            </div>

            {/* --- ANALYZE BUTTON --- */}
            <div className="buttons">
                <button
                    onClick={handleScan}
                    disabled={isLoading}
                    className="scan-button"
                >
                    {isLoading ? 'Analyzing Data...' : 'Analyze Match'}
                </button>
            </div>
        </>
    );
}
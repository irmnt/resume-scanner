import { useState } from 'react'
import './App.css'

function App() {

  // State of the resume text, job description text, and the analysis result
  const [resumeText, setResumeText] = useState<string>('');
  const [jdText, setJdText] = useState<string>('');
  const [result, setResult] = useState<ScanResponse | string | null>(null);

  /* Response schema */
  interface ScanResponse {
  result: string;
  missing_skills: string[];
  "your resume": string;     // Note: Keys with spaces need quotes!
  "job description": string;
  }

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

      // 3. Update the UI with the result
      console.log(data);
      setResult(data);

    } catch (error) {
      console.error('Error:', error);
      setResult("Error: Could not connect to scanner backend.");
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

      {/* Display the Result */}
      {result && (
        <div className="result-container"> {/* 1. Wrapped everything in a parent div */}
          
          {/* 2. Check: Is 'result' just an error string? */}
          {typeof result === 'string' ? (
            <p style={{ color: 'red' }}>{result}</p>
          ) : (
            /* 3. If it's not a string, it's our ScanResponse object */
            <>
              <div className="result-score">
                <h3>Analysis Result: </h3>
                <p>{result.result}</p>
              </div>

              <h4>Missing Skills:</h4>
              <ul>
                {result.missing_skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
              
              {/* Optional: Show parsed text to prove it worked */}
              <details>
                <summary>Debug Info</summary>
                <p>Resume length: {result["your resume"].length}</p>
              </details>
            </>
          )}
        </div>
      )}
    </>
  )
}

export default App

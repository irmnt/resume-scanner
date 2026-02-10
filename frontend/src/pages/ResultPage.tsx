import { useLocation, Link } from 'react-router-dom';


/* Response schema */
interface ScanResponse {
    result: string;
    missing_skills: string[];
    "your_resume": string;     // Note: Keys with spaces need quotes!
    "job_description": string;
}

export default function ResultPage() {
    const location = useLocation();

    const analysisData = location.state?.analysisData as ScanResponse;

    if (!analysisData) {
        return (
            <div>
                <h2>No analysis data found.</h2>
                <Link to="/">Go back to Home Page</Link>
            </div>
        );
    }

    return (
        <div>
      <h2>Analysis Complete</h2>
      
      <div className="result-score">
        <h3>Score:</h3>
        <p>{analysisData.result}</p>
      </div>

      <h4>Missing Skills:</h4>
      <ul>
        {analysisData.missing_skills.map((skill, index) => (
          <li key={index}>{skill}</li>
        ))}
      </ul>

      {/* A button to go back to the home page */}
      <Link to="/">
        <button style={{ marginTop: '20px' }}>Scan Another Resume</button>
      </Link>
    </div>
    );
}
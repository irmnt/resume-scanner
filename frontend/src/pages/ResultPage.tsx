import { useLocation, Link } from 'react-router-dom';


/* Response schema */
interface ScanResponse {
    status: string;
    match_score: string;        // e.g. "85.5%"
    missing_skills: string[];   
    details: {
        resume_length: number;  
        jd_length: number;      
    };
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
        <h3>Match Percentage:</h3>
        <p>{analysisData.match_score}</p>
      </div>

      <h4>Missing Skills:</h4>
      {analysisData.missing_skills && analysisData.missing_skills.length > 0 ? (
        <ul>
          {analysisData.missing_skills.map((skill, index) => (
            <li key={index}>{skill}</li>
          ))}
        </ul>
      ) : (
        <p>Great job! No major missing skills identified.</p>
      )}

      <div className="details">
        <p>Characters analyzed; {analysisData.details.resume_length} (Resume) / {analysisData.details.jd_length} (JD)</p>
      </div>

      {/* A button to go back to the home page */}
      <Link to="/">
        <button style={{ marginTop: '20px' }}>Scan Another Resume</button>
      </Link>
    </div>
    );
}
import { useLocation, Link } from 'react-router-dom';

interface ExperienceEvaluation {
    requirement: string;
    status: string;
    details: string;
}


/* Response schema */
interface ScanResponse {
    status: string;
    match_score: string;        // e.g. "85.5%"
    missing_skills: string[]; 
    experience_analysis: ExperienceEvaluation[];
    details: {
        resume_skills_found: string[];
        jd_skills_required: string[];
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
      <h1>Analysis Complete!</h1>
      
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

      <h4>Experience Evaluation:</h4>
      {analysisData.experience_analysis && analysisData.experience_analysis.length > 0 ? (
        <ul>
          {analysisData.experience_analysis.map((exp, index) => (
            <li key={index}>
              <p><strong>Requirement:</strong> {exp.requirement}</p>
              <p><strong>Status:</strong> {exp.status}</p>
              <p><strong>Details:</strong> {exp.details}</p>

            </li>
          ))}
        </ul>
      ) : (
        <p>No specific years of experiece mentioned in the Job Description.</p>
      )}

      {/* 4. Updated Details Section */}
      <div className="details" style={{ marginTop: '20px', fontSize: '0.8rem', color: '#666' }}>
        <p>Skills extracted from your resume: {analysisData.details.resume_skills_found.join(', ') || 'None'}</p>
      </div>

      {/* A button to go back to the home page */}
      <Link to="/">
        <button style={{ marginTop: '20px' }}>Scan Another Resume</button>
      </Link>
    </div>
    );
}
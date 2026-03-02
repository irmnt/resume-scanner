import { useLocation, Link } from 'react-router-dom';

interface ExperienceEvaluation {
  requirement: string;
  status: string;
  details: string;
}

/* Response schema */
interface ScanResponse {
  status: string;
  match_score: string;
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
      <div className="result-container empty-state">
        <h2>No analysis data found.</h2>
        <Link to="/">
          <button className="submit-button">Go back to Home Page</button>
        </Link>
      </div>
    );
  }

  // Helper function to dynamically color the experience cards based on ATS feedback
  const getStatusClass = (status: string) => {
    if (status.includes("Qualified")) return "status-pass";
    if (status.includes("Partially") || status.includes("Years")) return "status-warn";
    return "status-fail";
  };

  return (
    <div className="result-container">
      <h1>Analysis Complete!</h1>

      {/* --- SCORE SECTION --- */}
      <div className="score-card">
        <h3>Match Percentage</h3>
        <p className="score-number">{analysisData.match_score}</p>
      </div>

      <div className="analysis-grid">
        {/* --- MISSING SKILLS SECTION --- */}
        <div className="analysis-section missing-skills-section">
          <h4>Missing Skills</h4>
          {analysisData.missing_skills && analysisData.missing_skills.length > 0 ? (
            <ul className="skills-list">
              {analysisData.missing_skills.map((skill, index) => (
                <li key={index} className="skill-tag">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="success-text">Great job! No major missing skills identified.</p>
          )}
        </div>

        {/* --- EXPERIENCE SECTION --- */}
        <div className="analysis-section experience-section">
          <h4>Experience Evaluation</h4>
          {analysisData.experience_analysis && analysisData.experience_analysis.length > 0 ? (
            <ul className="experience-list">
              {analysisData.experience_analysis.map((exp, index) => (
                <li key={index} className={`experience-card ${getStatusClass(exp.status)}`}>
                  <p className="exp-req"><strong>Requirement:</strong> {exp.requirement}</p>
                  <p className="exp-status"><strong>Status:</strong> {exp.status}</p>
                  <p className="exp-details"><em>{exp.details}</em></p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="neutral-text">No specific years of experience mentioned in the Job Description.</p>
          )}
        </div>

        {/* --- EXTRACTED DETAILS --- */}
        <div className="analysis-section skills-section">
          <h4>Skills Extracted</h4>
          {analysisData.details.resume_skills_found && analysisData.details.resume_skills_found.length > 0 ? (
            <ul className="extracted-list">
              {analysisData.details.resume_skills_found.map((skill, index) => (
                <li key={index} className="extracted-tag">{skill}</li>
              ))}
            </ul>
          ) : (
            <p className="neutral-text">No specific skills are extracted.</p>
          )}
        </div>
      </div>


      {/* --- NAVIGATION --- */}
      <div className="buttons">
        <Link to="/">
          <button className="submit-button secondary-button">Scan Another Resume</button>
        </Link>
      </div>
    </div>
  );
}
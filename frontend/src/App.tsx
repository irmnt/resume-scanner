import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>RESUME SCANNER</h1>
      <div className="resume-input">
        <h4>Input your resume here</h4>
        <textarea 
        id="resume-text"
        rows={10}       // Sets initial height (in lines of text)
        placeholder="Copy and paste your resume text here..."
        className="resizable-box"
      />
      </div>
      <div className="jd-input">
        <h4>Input the job description here</h4>
        <textarea 
        id="jd-text"
        rows={10}       // Sets initial height (in lines of text)
        placeholder="Copy and paste the job description here..."
        className="resizable-box"
      />
      </div>
      <div className="buttons">
        <button>Analyze</button>
      </div>
    </>
  )
}

export default App

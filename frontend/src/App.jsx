import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Custom CSS file

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleMatch = async () => {
    if (!resume || !jobDescription.trim()) {
      alert("Please upload a resume and paste job description");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/match/", formData);
      setResult(res.data);
    } catch (err) {
      alert("Error connecting to server");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">Resume Matcher</header>

      <div className="upload-section">
        <label>Choose file</label>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setResume(e.target.files[0])}
        />
      </div>

      <div className="content">
        <div className="left">
          <h2>Job Description</h2>
          <textarea
            placeholder="Please paste job description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>
        <div className="right">
          <h2>Result</h2>
          {result ? (
            <div className="result-box">
              <p><strong>Match Score:</strong> {result.match_score}</p>
              <p><strong>Resume Skills:</strong> {result.resume_skills.join(", ") || "None"}</p>
              <p><strong>Missing Skills:</strong> {result.missing_skills.join(", ") || "None"}</p>
              <p className="feedback">{result.feedback}</p>

              {result.suggested_keywords && (
                <>
                  <strong>Suggested Keywords:</strong>
                  <ul>
                    {result.suggested_keywords.map((kw, idx) => (
                      <li key={idx}>{kw}</li>
                    ))}
                  </ul>
                </>
              )}

              {result.improvements?.length > 0 && (
                <>
                  <strong>Improvements:</strong>
                  <ul>
                    {result.improvements.map((imp, idx) => (
                      <li key={idx}>{imp}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          ) : (
            <p className="placeholder">Let's know what is missing</p>
          )}
        </div>
      </div>

      <div className="button-section">
        <button onClick={handleMatch} disabled={loading}>
          {loading ? "Matching..." : "Match"}
        </button>
      </div>
    </div>
  );
}

export default App;

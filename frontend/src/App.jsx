import React, { useState } from 'react';
import './App.css'; // Import the new CSS file

function App() {
  const [file, setFile] = useState(null);
  const [topK, setTopK] = useState(5);
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [fileName, setFileName] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setRecommendations([]);
      setError('');
    }
  };

  const handleTopKChange = (event) => {
    const value = Math.max(1, Math.min(20, Number(event.target.value)));
    setTopK(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setRecommendations([]);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://localhost:8000/recommend?top_k=${topK}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to get recommendations.');
      }
      
      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Binge Next</h1>
        <p>Upload your Netflix viewing history to get personalized recommendations.</p>
      </header>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label htmlFor="file-upload">Upload History File (.csv)</label>
          <input id="file-upload" type="file" onChange={handleFileChange} accept=".csv" style={{display: 'none'}} />
          <button type="button" onClick={() => document.getElementById('file-upload').click()} style={{width: '100%', padding: '10px', border: '1px dashed #ccc', borderRadius: '4px'}}>
            {fileName || 'Choose a file...'}
          </button>
        </div>

        <div className="form-group">
          <label htmlFor="topKInput">Number of Recommendations</label>
          <input
            id="topKInput"
            type="number"
            value={topK}
            onChange={handleTopKChange}
            min="1"
            max="20"
          />
        </div>
        
        <button type="submit" className="submit-btn" disabled={isLoading || !file}>
          Get Recommendations
        </button>
      </form>

      {isLoading && <div className="loading-spinner"></div>}
      {error && <p className="error-message">{error}</p>}

      {recommendations.length > 0 && (
        <div className="recommendations-container">
          <h2>Your Top {topK} Recommendations</h2>
          <ul className="recommendations-list">
            {recommendations.map((rec, index) => (
              <li key={index} className="recommendation-card">
                <strong>{rec.title}</strong>
                <span className="director"> ({rec.director})</span>
                <em className="genre">{rec.genre}</em>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
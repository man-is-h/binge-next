import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [topK, setTopK] = useState(5); // Add state for top_k
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setRecommendations([]);
    setError('');
  };

  const handleTopKChange = (event) => {
    // Ensure the value is within the allowed range (1-20)
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

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Construct the URL dynamically with the topK value from state
      const response = await fetch(`http://localhost:8000/recommend?top_k=${topK}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Something went wrong');
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
    <div style={{ fontFamily: 'sans-serif', maxWidth: '600px', margin: 'auto', padding: '20px' }}>
      <h1>Movie Recommender</h1>
      <p>Upload your viewing history file (e.g., NetflixViewingHistory.csv) to get recommendations.</p>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="topKInput">Number of Recommendations (1-20): </label>
          <input
            id="topKInput"
            type="number"
            value={topK}
            onChange={handleTopKChange}
            min="1"
            max="20"
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input type="file" onChange={handleFileChange} accept=".csv" />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Getting Recommendations...' : 'Get Recommendations'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {recommendations.length > 0 && (
        <div>
          <h2>Your Top {topK} Recommendations:</h2>
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {recommendations.map((rec, index) => (
              <li key={index} style={{ border: '1px solid #ccc', padding: '10px', margin: '5px 0', borderRadius: '5px' }}>
                <strong>{rec.title}</strong> ({rec.genre}) - Directed By <em>{rec.director}</em>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
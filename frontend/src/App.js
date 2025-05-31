import { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(""); // Clear previous errors
    setVideoUrl(""); // Clear previous video

    try {
      const res = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt,
          generate_audio: false
        })
      });
      
      if (!res.ok) {
        throw new Error("Failed to get response from server");
      }
      
      const data = await res.json();

      if (data.error) {
        throw new Error(data.error);
      }

      if (data.video_url) {
        setVideoUrl(`${API_BASE_URL}${data.video_url}`);
      } else {
        throw new Error("No visualization was generated");
      }
    } catch (error) {
      console.error("Error querying API: ", error);
      setError(error.message || "Failed to generate visualization");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>Math Visualizer AI</h1>
        <p className="subtitle">Create animated math visualizations with AI</p>
      </header>

      <main>
        <section className="input-section">
          <form onSubmit={handleSubmit}>
            <textarea 
              placeholder="Describe the mathematical concept you want to visualize..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="prompt-textarea"
            />
            <button 
              type="submit" 
              className="submit-button"
              disabled={isLoading || !prompt.trim()}
            >
              {isLoading ? "Generating..." : "Visualize"}
            </button>
          </form>
        </section>

        {isLoading && (
          <section className="output-section">
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Generating your math visualization...</p>
            </div>
          </section>
        )}

        {!isLoading && error && (
          <section className="output-section error-section">
            <h2>Generation Failed</h2>
            <p className="error-message">{error}</p>
            <p className="retry-message">Please try modifying your prompt and try again.</p>
          </section>
        )}

        {!isLoading && videoUrl && (
          <section className="output-section">
            <h2>Generated Visualization</h2>
            <div className="video-container">
              <video 
                controls 
                width="480px"
                src={videoUrl}
                className="video-player" 
              >
                Your browser does not support the video tag.
              </video>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
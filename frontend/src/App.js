import { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:4000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({prompt})
      });
      if (!res.ok) {
        throw new Error("Failed to get response");
      }
      const data = await res.json();

      if (data.video_url) {
        setVideoUrl(`http://localhost:4000${data.video_url}`);
      }
    } catch (error) {
      console.error("Error querying API: ", error);
    }
  }

  return (
    <div className="App">
      <h1>Math Vizualizer AI</h1>
      <form onSubmit={handleSubmit}>
        <textarea 
          placeholder="Enter your problem..."
          onChange={(e) => setPrompt(e.target.value)}
        />
        <div>
          <button type="submit">Submit button</button>
        </div>
      </form>

      <div>
        <h2>Generated Video:</h2>
        {videoUrl ? (
          <video 
            controls 
            width="100%"
            src={videoUrl} 
            type="video/mp4"
          >
            Your browser does not support the video tag.
          </video>
        ) : (
          <p>No video available yet</p>
        )}
      </div>
    </div>
  );
}

export default App;
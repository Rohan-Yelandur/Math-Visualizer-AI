import { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

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
      setResponse(data);
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
        <h2>Reponse: </h2>
        <div>{response}</div>
      </div>
    </div>
  );
}

export default App;

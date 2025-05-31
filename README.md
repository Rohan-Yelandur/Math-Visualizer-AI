# Math Visualizaion AI
Check it out here: https://math-visualizer-ai.vercel.app/
An AI that truly teaches you math concepts. You are walked through the steps for solving a problem while seeing and hearing the solutions.

Frontend deployed on vercel. Backend deployed on Render.


## Local Setup

### Frontend
Install Dependencies
```bash
npm install
```
Create .env file at folder root and add the following
```bash
REACT_APP_API_BASE_URL=http://localhost:{same port that backend is running on}
```

### Backend
Install Dependencies
```bash
npm install
```

Create .env file at folder root and add the following
```bash
GEMINI_API_KEY=yourapikey
PORT=portnumber
```
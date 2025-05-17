const express = require("express");
const dotenv = require("dotenv");
const {GoogleGenAI} = require("@google/genai");
const cors = require("cors");
const {SYSTEM_INSTRUCTIONS} = require("./prompts.js");

dotenv.config()
const app = express();

app.use(express.json());
app.use(cors());

const ai = new GoogleGenAI({ apiKey: Wprocess.env.GEMINI_API_KEY });

app.get("/", (req, res) => {
    res.send("Math AI Backend");
})

app.post("/query", async(req, res) => {
    try {
        const {prompt} = req.body;
        if (!prompt) {
            return res.status(400).json({error: "Prompt not provided"});
        }

        const response = await ai.models.generateContent({
            model: "gemini-2.0-flash",
            contents: prompt,
            config: {
                systemInstruction: SYSTEM_INSTRUCTIONS,
            }
        });

        res.json(response.text);
    } catch (error) {
        console.error("Error querying Gemini API: ", error);
        res.status(500).json({error: "Failed to query Gemini API"});
    }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
});
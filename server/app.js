import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import data from "./dashboard.json" with { type: "json" };
import { analyzeDashboard } from "./ai.js";
import { runAnalyticsAgent } from "./agent/analyticsAgent.js";

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

// Existing endpoint
app.get("/dashboard", (req, res) => {
  res.json(data);
});

// New AI endpoint
app.post("/analyze", async (req, res) => {

  try {

    const { question } = req.body;

    if (!question) {

      return res.status(400).json({
        success: false,
        message: "Question is required"
      });

    }


    const answer = await runAnalyticsAgent(
      question,
      data
    );


    res.json({
      success: true,
      answer
    });

  } catch (error) {

    console.error(error);

    res.status(500).json({
      success: false,
      message: "AI analysis failed"
    });

  }

});
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from run_agent import (
    initialize_agent,
    run_agent
)

# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="AI Dashboard Analytics API"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# --------------------------------------------------
# Load dashboard data
# --------------------------------------------------

with open(
    "dashboard.json",
    "r",
    encoding="utf-8"
) as file:

    dashboard_data = json.load(file)


# --------------------------------------------------
# Initialize agent ONCE
# --------------------------------------------------

initialize_agent(
    dashboard_data
)


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "AI Dashboard Analytics API is running"
    }

# --------------------------------------------------
# Dashboard API
# --------------------------------------------------

@app.get("/dashboard")
def get_dashboard():

    return dashboard_data

# --------------------------------------------------
# Analyze endpoint
# --------------------------------------------------

@app.post("/analyze")
def analyze_dashboard(
    request: dict
):

    question = request.get(
        "question",
        ""
    )

    conversation_id = request.get(
        "conversation_id",
        "default"
    )


    # --------------------------------------------------
    # Validate question
    # --------------------------------------------------

    if not question.strip():

        return {
            "success": False,
            "answer": "",
            "message": "Question is required"
        }


    # --------------------------------------------------
    # Run AI agent
    # --------------------------------------------------

    try:

        answer = run_agent(
            question=question,
            conversation_id=conversation_id
        )

        return {
            "success": True,
            "answer": answer
        }


    except Exception as error:

        print(
            "Agent error:",
            error
        )

        return {
            "success": False,
            "answer": "",
            "message": str(error)
        }
# main.py
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
import config
# Import schemas and the core logic function
from schemas import input_output_schema
from llm import logic

# Load environment variables (e.g., GOOGLE_API_KEY) from .env file
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

@app.post("/recommend", response_model=input_output_schema.RecommendationResponses)
async def recommend_crop(user_input: input_output_schema.UserInput):
    """
    Receives farmer's input and returns a ranked list of crop recommendations.
    """
    try:
        recommendations = logic.generate_recommendation(user_input)
        return recommendations
    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations.")

# Optional: Add a root endpoint for health checks
@app.get("/")
def read_root():
    return {"status": "API is running"}
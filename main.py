from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
import config
from schemas import input_output_schema
from llm import logic

load_dotenv()

llm_api_key = os.getenv("GOOGLE_API_KEY")
if not llm_api_key:
    raise ValueError("Google api key not found in environment file.")
os.environ["GOOGLE_API_KEY"] = llm_api_key

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
        print(f"An error occurred: {e}")
        print(f"Error type: {type(e).__name__}")  # This helps debugging
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")


# Optional: Add a root endpoint for health checks
@app.get("/")
def read_root():
    return {"status": "API is running"}
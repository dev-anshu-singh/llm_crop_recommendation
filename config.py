import os
from pathlib import Path

# --- API Configuration ---
API_TITLE = "Crop Recommendation API"
API_DESCRIPTION = "An API to provide intelligent crop recommendations for farmers in India."
API_VERSION = "1.0.0"

# --- LLM and Embedding Model Configuration ---
GEMINI_LLM_MODEL = "gemini-2.5-pro"
EMBEDDING_MODEL = "models/gemini-embedding-001"

BASE_DIR = Path(__file__).resolve().parent
# --- RAG and Vector Store Configuration ---
FAISS_INDEX_PATH = BASE_DIR/"llm"/"faiss_index"

# --- Data File Paths ---
DATA_DIR = BASE_DIR / "data"

AGRO_ZONE_DATA_PATH = os.path.join(DATA_DIR, "agro_climatic_zone.json")
FERTILIZER_DATA_PATH = os.path.join(DATA_DIR, "fertilizer_recommendations.csv")
MSP_DATA_PATH = os.path.join(DATA_DIR, "msp_prices_2024_25.json")
IRRIGATION_AREA_PATH = os.path.join(DATA_DIR, "District_wise_irrigation_area.csv")
LABOUR_COST_PATH = os.path.join(DATA_DIR, "District_wise_labour_cost.csv")
NORMAL_RAINFALL_PATH = os.path.join(DATA_DIR, "District_wise_normal_rainfall.csv")
CROP_PRODUCTION_PATH = os.path.join(DATA_DIR, "district_wise_production.csv")
GROUND_WATER_LEVEL_PATH = os.path.join(DATA_DIR, "District_Wise_Pre_Monsoon_Post_Monsoon_Water_Levels_1755802403703.xlsx")

# --- External API Configuration ---
SOIL_API_BASE_URL = "https://rest-sisindia.isric.org/sisindia/v1.0"
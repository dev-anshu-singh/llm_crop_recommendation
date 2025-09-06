from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import config
from schemas.input_output_schema import RecommendationResponses
from dotenv import load_dotenv

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(model=config.GEMINI_LLM_MODEL)
gemini_embedding_model = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)
gemini_structured_llm = gemini_llm.with_structured_output(RecommendationResponses)

# llm_model.py
#
# import os
# from dotenv import load_dotenv
#
# # Load variables from the .env file into the environment
# load_dotenv()
#
# # --- Rest of your existing code ---
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# import config
# from schemas.input_output_schema import RecommendationResponses
#
# # Get the API key from the now-loaded environment
# api_key = os.getenv("GOOGLE_API_KEY")
#
# # Pass the key to the model initializers
# gemini_llm = ChatGoogleGenerativeAI(
#     model=config.GEMINI_LLM_MODEL,
#     google_api_key=api_key
# )
#
# gemini_embedding_model = GoogleGenerativeAIEmbeddings(
#     model=config.EMBEDDING_MODEL,
#     google_api_key=api_key
# )
#
# gemini_structured_llm = gemini_llm.with_structured_output(RecommendationResponses)
#
# # print("LLM models initialized successfully!")
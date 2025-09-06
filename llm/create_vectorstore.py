import warnings
from langchain_community.vectorstores import FAISS
from rag_knowledge_base_loader import load_agro_zone_knowledge_base
from langchain_core._api.deprecation import LangChainDeprecationWarning
warnings.filterwarnings("ignore",category=LangChainDeprecationWarning)
from dotenv import load_dotenv
import llm_model

load_dotenv()

knowledge_documents = []
knowledge_documents.extend(load_agro_zone_knowledge_base())

print("Creating Vector Store...")

vector_store = FAISS.from_documents(
    embedding=llm_model.gemini_embedding_model,
    documents=knowledge_documents
)

vector_store.save_local("faiss_index")
print("Vector store created and saved to 'faiss_index' folder.")
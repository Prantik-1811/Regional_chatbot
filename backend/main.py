from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse
from rag import RAGPipeline
import uvicorn

app = FastAPI(title="HK Cyber Intelligence Chatbot")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
try:
    rag = RAGPipeline()
except Exception as e:
    print(f"Error initializing RAG pipeline: {e}")
    rag = None

@app.get("/")
async def root():
    return {"message": "HK Cyber Intelligence Chatbot API is running"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if not rag:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized")
    
    answer, sources = rag.query(request.query, request.region)
    return QueryResponse(answer=answer, sources=sources)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

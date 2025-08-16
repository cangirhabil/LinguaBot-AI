from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import List, Optional
import uvicorn

from models import IngestRequest, QueryRequest, IngestResponse, QueryResponse
from services.ai_service import AIService
from services.auth_service import verify_api_key

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Multilingual Chatbot AI Service",
    description="AI service for multilingual chatbot SaaS platform",
    version="1.0.0"
)

# CORS middleware - Node.js backend'den gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4000"],  # Node.js ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Service instance
ai_service = AIService()

@app.on_event("startup")
async def startup_event():
    """Initialize AI service on startup"""
    await ai_service.initialize()

@app.get("/")
async def root():
    return {"message": "Multilingual Chatbot AI Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-service"}

@app.post("/v1/ingest", response_model=IngestResponse)
async def ingest_data(
    request: IngestRequest,
    _: bool = Depends(verify_api_key)
):
    """
    SSS verilerini işleyip Pinecone vektör veritabanına depolar.
    
    Args:
        request: SSS listesi ve kullanıcı ID'si
        
    Returns:
        IngestResponse: İşlem durumu
    """
    try:
        success = await ai_service.ingest_faqs(request.faqs, request.user_id)
        if success:
            return IngestResponse(status="success", message="Data ingested successfully")
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/v1/query", response_model=QueryResponse)
async def query_bot(
    request: QueryRequest,
    _: bool = Depends(verify_api_key)
):
    """
    Kullanıcı sorularını işleyip çoklu dil desteğiyle yanıt verir.
    
    Args:
        request: Kullanıcı sorusu ve bot/kullanıcı ID'si
        
    Returns:
        QueryResponse: AI'dan gelen yanıt
    """
    try:
        answer = await ai_service.query(request.message, request.user_id)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

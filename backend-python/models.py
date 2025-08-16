from pydantic import BaseModel, Field
from typing import List, Optional

class FAQ(BaseModel):
    """Tek bir SSS modeli"""
    question: str = Field(..., description="Soru metni")
    answer: str = Field(..., description="Cevap metni")

class IngestRequest(BaseModel):
    """SSS verilerini işleme isteği"""
    faqs: List[FAQ] = Field(..., description="SSS listesi")
    user_id: str = Field(..., description="Kullanıcı ID'si")

class IngestResponse(BaseModel):
    """SSS işleme yanıtı"""
    status: str = Field(..., description="İşlem durumu")
    message: str = Field(..., description="İşlem mesajı")

class QueryRequest(BaseModel):
    """Soru sorma isteği"""
    message: str = Field(..., description="Kullanıcının sorusu")
    user_id: str = Field(..., description="Bot/Kullanıcı ID'si")

class QueryResponse(BaseModel):
    """Soru yanıtı"""
    answer: str = Field(..., description="AI'dan gelen cevap")

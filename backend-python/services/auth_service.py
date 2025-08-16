from fastapi import HTTPException, Header
import os

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-KEY")):
    """
    Node.js backend'den gelen istekleri doğrular.
    
    Args:
        x_api_key: Header'dan gelen API anahtarı
        
    Returns:
        bool: Doğrulama başarılı ise True
        
    Raises:
        HTTPException: Geçersiz API anahtarı durumunda
    """
    expected_key = os.getenv("API_KEY")
    
    if not expected_key:
        raise HTTPException(
            status_code=500, 
            detail="API key not configured"
        )
    
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key"
        )
    
    return True

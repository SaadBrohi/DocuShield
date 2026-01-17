from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentResponse(BaseModel):
    id: str
    filename: str
    risk_score: Optional[int] = None
    processed: bool = False

class RiskAnalysisRequest(BaseModel):
    document_id: str

class RiskAnalysisResponse(BaseModel):
    document_id: str
    risk_score: int
    risk_level: str
    flagged_clauses: List[Dict[str, Any]]
    explanation: str

class ChatRequest(BaseModel):
    document_id: str
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

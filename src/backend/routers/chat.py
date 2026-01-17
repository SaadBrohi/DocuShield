from fastapi import APIRouter, HTTPException
from src.backend.services.pipeline_service import PipelineService
from src.backend.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])
pipeline = PipelineService()

@router.post("/", response_model=ChatResponse)
async def chat_document(request: ChatRequest):
    try:
        answer = pipeline.query_document(request.document_id, request.query)
        # In a real app we'd return sources too, currently simple string response
        return ChatResponse(answer=answer, sources=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

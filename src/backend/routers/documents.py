from fastapi import APIRouter, UploadFile, File, HTTPException
from src.backend.services.pipeline_service import PipelineService
from src.backend.models.schemas import DocumentResponse, RiskAnalysisResponse, RiskAnalysisRequest

router = APIRouter(prefix="/documents", tags=["documents"])
pipeline = PipelineService()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        content = await file.read()
        doc_id = pipeline.process_upload(content, file.filename)
        return DocumentResponse(id=doc_id, filename=file.filename, processed=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[DocumentResponse])
async def list_documents():
    # Simple list from directory for MVP
    import os
    docs = []
    # This is a hacky way to populate the list, ideally use a DB
    raw_dir = "data/raw"
    if os.path.exists(raw_dir):
        for f in os.listdir(raw_dir):
            if f.endswith((".pdf", ".docx")):
                 # We don't have the original filename map if we renamed to UUID, 
                 # but in pipeline_service I saved as {uuid}.pdf.
                 # Wait, in pipeline_service, I saved as uuid.ext.
                 # I lost the original filename mapping unless I store it.
                 # pipeline_service.process_upload calls save_text with doc_id.
                 pass
    
    # Better approach: Just list ids for now or scan processed text files
    processed_dir = "data/processed"
    if os.path.exists(processed_dir):
        for f in os.listdir(processed_dir):
             if f.endswith(".txt"):
                 doc_id = f.replace(".txt", "")
                 docs.append(DocumentResponse(id=doc_id, filename=f"Document {doc_id[:8]}...", processed=True))
    return docs

@router.post("/{doc_id}/analyze", response_model=RiskAnalysisResponse)
async def analyze_document_risk(doc_id: str):
    try:
        result = pipeline.analyze_document(doc_id)
        return RiskAnalysisResponse(document_id=doc_id, **result)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

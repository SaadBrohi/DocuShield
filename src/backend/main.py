from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="DocuShield API",
    description="Backend for DocuShield Hybrid AI Document Risk Analysis System",
    version="0.1.0"
)

# Instrument Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DocuShield API is running", "status": "ok"}

from src.backend.routers import documents, chat

app.include_router(documents.router)
app.include_router(chat.router)

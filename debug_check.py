import os
import sys
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.getcwd())

load_dotenv()

print("--- Debugging Environment ---")
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("ERROR: GROQ_API_KEY is missing!")
else:
    print(f"GROQ_API_KEY found: {api_key[:5]}...")

print("\n--- Testing LLM Service ---")
try:
    from src.backend.services.llm_service import LLMService
    service = LLMService()
    print("LLMService initialized without error.")
    
    print("Testing analyze_risk...")
    result = service.analyze_risk("This Agreement shall be terminated immediately if the Provider fails to deliver.")
    print("Result:", result)
except Exception as e:
    print(f"ERROR in LLM Service: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Testing Pipeline Service (Local) ---")
try:
    from src.backend.services.pipeline_service import PipelineService
    pipeline = PipelineService()
    print("PipelineService initialized.")
except Exception as e:
    print(f"ERROR in Pipeline Service: {e}")
    traceback.print_exc()

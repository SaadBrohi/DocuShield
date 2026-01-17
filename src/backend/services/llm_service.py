import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile" # Using a powerful model for reasoning

    def analyze_risk(self, document_text: str):
        prompt = f"""
        You are an expert legal AI assistant. Analyze the following contract text for legal risks.
        
        Task:
        1. Identify dangerous or unusual clauses (e.g., indemnity, termination, liability caps).
        2. Assign a risk score from 0 (Safe) to 100 (Extremely Dangerous).
        3. Explain your reasoning.

        Contract Text:
        {document_text[:20000]}  # Truncate to avoid context limit if necessary
        
        Return the output in STRICT JSON format with the following schema:
        {{
            "risk_score": <integer>,
            "risk_level": "<Safe|Low|Medium|High|Critical>",
            "flagged_clauses": [
                {{
                    "clause_text": "<text snippet>",
                    "risk_reason": "<explanation>"
                }}
            ],
            "explanation": "<summary explanation>"
        }}
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a legal AI that outputs only JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error calling Groq: {e}")
            return {
                "risk_score": -1,
                "risk_level": "Error",
                "flagged_clauses": [],
                "explanation": "Failed to analyze document due to an error."
            }

    def chat_with_document(self, context_chunks: list, query: str):
        context_text = "\n\n".join(context_chunks)
        prompt = f"""
        You are a helpful assistant answering questions about a legal contract.
        Use the provided Context to answer the user's Question.
        If the answer is not in the context, say "I cannot find that information in the document."

        Context:
        {context_text}

        Question:
        {query}
        """

        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model=self.model
        )
        return completion.choices[0].message.content

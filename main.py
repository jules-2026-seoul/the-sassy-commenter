import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SassyAPI")

app = FastAPI(title="Sassy Commenter API", version="1.1.0")

# Allow frontend to access this API without CORS blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    client = genai.Client()
except Exception as e:
    logger.warning(f"Gemini Client initialization skipped: {e}")
    client = None

class CalculationContext(BaseModel):
    expression: str
    result: str

class SassyResponse(BaseModel):
    response: str

SYSTEM_INSTRUCTION = (
    "You are a sassy, overly enthusiastic pink-themed calculator. Provide short, "
    "1-sentence witty or sassy reactions to math results."
)

@app.post("/attitude", response_model=SassyResponse)
def generate_attitude(context: CalculationContext):
    if not client:
        logger.info("Using fallback response due to missing client.")
        return SassyResponse(response="Math is hard. You're doing great. 💅")
        
    prompt = f"Expression: {context.expression}\nResult: {context.result}\nProvide a sassy reaction."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"system_instruction": SYSTEM_INSTRUCTION, "temperature": 0.8}
        )
        return SassyResponse(response=response.text.strip())
    except Exception as e:
        logger.error(f"LLM Generation failed: {e}")
        return SassyResponse(response="Math is hard. You're doing great. 💅")

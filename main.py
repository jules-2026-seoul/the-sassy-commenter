import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai.errors import APIError

app = FastAPI(title="Sassy Commenter API")

# Initialize the Gemini client. It will automatically check the GEMINI_API_KEY environment
# variable, or fall back to Application Default Credentials on Google Cloud.
try:
    client = genai.Client()
except Exception as e:
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
        # Graceful fallback if client couldn't be initialized
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
        # Fallback phrase when the LLM call fails or key is invalid
        return SassyResponse(response="Math is hard. You're doing great. 💅")

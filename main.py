from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if present

app = FastAPI()

# The Gemini API key should be set as the environment variable GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) # client = genai.Client() --- IGNORE ---

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.prompt
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "MCP Gemini Model Server is running."}

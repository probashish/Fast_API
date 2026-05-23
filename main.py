import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client using environment variables
# Set OPENAI_API_KEY in Render's dashboard settings
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("nexus_api_key")
if not api_key:
    raise RuntimeError(
        "Missing OpenAI API key. Set OPENAI_API_KEY or nexus_api_key in your environment."
    )

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://apidev.navigatelabsai.com"
)

class PromptRequest(BaseModel):
    user_prompt: str

@app.get("/")
def read_root():
    return {"message": "NexusAI is working"}

@app.post("/run_task/")
async def run_task(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a personal AI tutor. Explain content provided by the user in layman's terms. Keep the response short and precise. Do not hallucinate."},
                {"role": "user", "content": req.user_prompt}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
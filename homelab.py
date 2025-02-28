from fastapi import FastAPI
import requests
from gtts import gTTS
import os

app = FastAPI()
tts = Piper(model="en_US-medium")

# Ollama API endpoint (adjust if running on a different server)
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/query")
def query_ai(prompt: str):
    # Send prompt to Ollama
    payload = {
        "model": "llama3",  # Change to your preferred Ollama model
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response_text = response.json()["response"]
    
    # Convert AI response to speech
    tts.speak(response_text)
    
    return {"response": response_text}

# Run the AI assistant API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

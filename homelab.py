from fastapi import FastAPI, Request
import requests
from gtts import gTTS
import os

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/query")
async def query_ai(request: Request):
    # Read raw JSON body
    body = await request.json()
    prompt = body.get("prompt")

    if not prompt:
        return {"error": "Prompt field is required"}

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    # Assuming the external API responds with a "response" key
    response_text = response.json().get("response", "")
    
    # Convert to speech with gTTS
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Play audio (install mpg123: sudo apt install mpg123)
    
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

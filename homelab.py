from fastapi import FastAPI
from pydantic import BaseModel
import requests
from gtts import gTTS
import os

# Define a request body model
class QueryRequest(BaseModel):
    prompt: str

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/query")
def query_ai(request: QueryRequest):
    prompt = request.prompt  # Access the prompt from the request body

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    # Make the request to the external API
    response = requests.post(OLLAMA_URL, json=payload)

    # Extract the response text from the external API response
    response_text = response.json().get("response", "")

    # Convert the response text to speech with gTTS
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Play audio (install mpg123: sudo apt install mpg123)
    
    # Return the text response as JSON
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

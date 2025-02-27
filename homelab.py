from fastapi import FastAPI
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()
model = AutoModelForCausalLM.from_pretrained("mistral-7b")
tokenizer = AutoTokenizer.from_pretrained("mistral-7b")

@app.post("/query")
def query_ai(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    return {"response": tokenizer.decode(outputs[0])}

# Run the AI assistant API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
app = FastAPI()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return response in plain text only. "
                    "Do not use markdown or special formatting."
                )
            },
            {
                "role": "user",
                "content": req.message
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    answer = completion.choices[0].message.content

    # ✅ REMOVE \n and clean text
    clean_answer = answer.replace("\n", " ").replace("\\n", " ")

    return {
        "question": req.message,
        "answer": clean_answer
    }
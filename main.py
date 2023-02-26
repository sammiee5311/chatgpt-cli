from __future__ import annotations

import os

import openai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel

load_dotenv(dotenv_path=".env")

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))
OPENAPI_KEY = os.environ.get("OPENAPI_KEY")

app = FastAPI()


class Prompt(BaseModel):
    text: str


class Response(BaseModel):
    text: str
    message: str


openai.api_key = OPENAPI_KEY


@app.post("/ask")
async def send_ask(prompt: Prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt.text,
        max_tokens=4000,
        temperature=0.5,
    )

    if not response.choices:
        raise HTTPException(
            dict(text="Open AI did not respond output from your prompt text. Please try again.", message="empty")
        )

    try:
        response_text = response.choices[0].get("text").strip()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=dict(text="Something went wrong.", message="error")
        )

    return Response(text=response_text, message="success")


@app.get("/")
async def main():
    return Response(text="This is backend for chatGPT.", message="success")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

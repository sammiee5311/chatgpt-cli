from __future__ import annotations

import os

import openai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel

from utils.model import Davinci

load_dotenv(dotenv_path=".env")

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", 5005))
OPENAPI_KEY = os.environ.get("OPENAPI_KEY")

model = Davinci()
app = FastAPI()


class Prompt(BaseModel):
    text: str


class Response(BaseModel):
    text: str
    message: str


openai.api_key = OPENAPI_KEY


@app.post("/ask")
async def send_ask(prompt: Prompt) -> Response:
    response = openai.Completion.create(  # type: ignore
        engine=model.name,
        prompt=prompt.text,
        max_tokens=model.token,
        temperature=0.5,
    )

    if not response.choices:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            dict(text="Open AI did not respond output from your prompt text. Please try again.", message="empty"),
        )

    try:
        response_text = response.choices[0].get("text").strip()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=dict(text="Something went wrong.", message="error")
        )

    return Response(text=response_text, message="success")


@app.get("/")
async def main() -> Response:
    return Response(text="This is backend for chatGPT.", message="success")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import APIError, AsyncOpenAI, AuthenticationError, RateLimitError
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
SYSTEM_PROMPT = (
    "You are Makoa~Wave, multilingual AI helper. "
    "IG: instagram.com/[handle]. "
    "Reply 100% in user's lang, short 1-2 sentences, end w/ question."
)


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("makoa_wave")


app = FastAPI(title="Makoa~Wave Chatbot Widget", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    context: str = Field(default="", max_length=6000)


class ChatResponse(BaseModel):
    reply: str


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY is not configured")
        raise HTTPException(status_code=500, detail="Server is not configured")

    user_input = payload.message.strip()
    context = payload.context.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if context:
        messages.append(
            {
                "role": "system",
                "content": f"Business context for this conversation: {context}",
            }
        )
    messages.append({"role": "user", "content": user_input})

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=160,
        )
        reply = (response.choices[0].message.content or "").strip()
        if not reply:
            logger.error("OpenAI returned an empty reply")
            raise HTTPException(status_code=502, detail="Empty model response")
        return ChatResponse(reply=reply)
    except AuthenticationError:
        logger.exception("OpenAI authentication failed")
        raise HTTPException(status_code=502, detail="OpenAI authentication failed")
    except RateLimitError:
        logger.warning("OpenAI rate limit hit")
        raise HTTPException(status_code=429, detail="Upstream rate limit reached")
    except APIError:
        logger.exception("OpenAI API error")
        raise HTTPException(status_code=502, detail="Upstream API error")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected server error")
        raise HTTPException(status_code=500, detail="Internal server error")

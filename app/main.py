import logging
import os
from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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


def _get_allowed_origins() -> list[str]:
    raw_value = os.getenv("ALLOWED_ORIGINS", "*").strip()
    if raw_value == "*":
        return ["*"]
    return [origin.strip() for origin in raw_value.split(",") if origin.strip()]


app = FastAPI(title="Makoa~Wave Chatbot Widget", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,
    max_retries=2,
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    context: str = Field(default="", max_length=6000)


class ChatResponse(BaseModel):
    reply: str


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request failure", extra={"path": request.url.path})
        raise

    duration_ms = round((perf_counter() - started_at) * 1000, 2)
    logger.info(
        "%s %s -> %s in %sms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(status_code=exc.status_code, content={"detail": detail})


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
    }


def _extract_reply_content(response) -> str:
    message = response.choices[0].message
    content = message.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text_value = getattr(item, "text", None)
            if text_value:
                parts.append(text_value)
        return "\n".join(parts).strip()
    return ""


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
                "role": "developer",
                "content": f"Business context for this conversation: {context}",
            }
        )
    messages.append({"role": "user", "content": user_input})

    try:
        logger.info("Submitting chat completion request")
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=160,
        )
        reply = _extract_reply_content(response)
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

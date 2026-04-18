import json
import os
from urllib import error, request

from fastapi import HTTPException, status

from Schemas.ai_chat import AIConsultRequest, AIConsultResponse

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-4o-mini"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing environment variable: {name}",
        )
    return value


def consult_with_ai(payload: AIConsultRequest) -> AIConsultResponse:
    api_key = _required_env("OPENROUTER_API_KEY")
    model = payload.model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
    referer = os.getenv("OPENROUTER_REFERER", "")
    app_title = os.getenv("OPENROUTER_APP_TITLE", "NomadAI")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if referer:
        headers["HTTP-Referer"] = referer
    if app_title:
        headers["X-OpenRouter-Title"] = app_title

    system_prompt = os.getenv(
        "OPENROUTER_SYSTEM_PROMPT",
        "You are NomadAI travel consultant. Answer shortly, clearly, and safely.",
    )

    messages = [msg.model_dump() for msg in payload.messages]
    if messages[0]["role"] != "system":
        messages.insert(0, {"role": "system", "content": system_prompt})

    body = {
        "model": model,
        "messages": messages,
        "temperature": payload.temperature,
    }

    req = request.Request(
        OPENROUTER_URL,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as response:
            raw_data = response.read().decode("utf-8")
            data = json.loads(raw_data)
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        raise HTTPException(
            status_code=exc.code if exc.code else 502,
            detail=f"OpenRouter error: {error_body or exc.reason}",
        ) from exc
    except error.URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenRouter connection error: {exc.reason}",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid JSON received from OpenRouter",
        ) from exc

    choices = data.get("choices", [])
    if not choices:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenRouter response has no choices",
        )

    answer = (choices[0].get("message") or {}).get("content", "")
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenRouter response has empty answer",
        )

    return AIConsultResponse(model=model, answer=answer)

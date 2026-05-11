# Makoa Wave Chatbot Widget

[![Release](https://img.shields.io/github/v/release/808cadger/makoa-wave-chatbot-widget?include_prereleases&label=release)](https://github.com/808cadger/makoa-wave-chatbot-widget/releases)
[![Last commit](https://img.shields.io/github/last-commit/808cadger/makoa-wave-chatbot-widget)](https://github.com/808cadger/makoa-wave-chatbot-widget/commits)
[![License](https://img.shields.io/github/license/808cadger/makoa-wave-chatbot-widget)](https://github.com/808cadger/makoa-wave-chatbot-widget/blob/HEAD/LICENSE)
![Platforms](https://img.shields.io/badge/platform-API%20service%2C%20Embeddable%20web%20widget-2563eb)

Deployable FastAPI chatbot widget with embeddable frontend and multilingual support hooks.

## Project Snapshot

| Area | Details |
|------|---------|
| Primary use case | Deployable FastAPI chatbot widget with embeddable frontend and multilingual support hooks. |
| Platforms | API service, Embeddable web widget |
| Core stack | Python, FastAPI, OpenAI API, JavaScript widget |
| Review first | `app` |

## Download Links

| Platform | Link |
|----------|------|
| iOS / iPhone | [Open the PWA in Safari](https://808cadger.github.io/makoa-wave-chatbot-widget/) and choose **Share -> Add to Home Screen** |
| Android | [Download the latest APK from GitHub Releases](https://github.com/808cadger/makoa-wave-chatbot-widget/releases/latest) |
| Source | [Download the GitHub source ZIP](https://github.com/808cadger/makoa-wave-chatbot-widget/archive/refs/heads/main.zip) |
| Repository | [View on GitHub](https://github.com/808cadger/makoa-wave-chatbot-widget) |

## Why This Repo Is Worth Reviewing

- Small, reviewable backend with a live demo endpoint.
- Embeddable widget pattern is easy to integrate into other apps.
- API contract is simple enough for quick deployment and testing.

<!-- INSTALL-START -->
## Install and run

These instructions install and run `makoa-wave-chatbot-widget` from a fresh clone.

### Clone
```bash
git clone https://github.com/808cadger/makoa-wave-chatbot-widget.git
cd makoa-wave-chatbot-widget
```

### Python/API service
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Notes
- Create any required `.env` file from `.env.example` before starting backend services.

### AI/API setup
- If the app has AI features, add the required provider key in the app settings or local `.env` file.
- Browser-only apps store user-provided API keys on the local device unless a backend endpoint is configured.

### License
- Apache License 2.0. See [`LICENSE`](./LICENSE).
<!-- INSTALL-END -->


Deployable FastAPI MVP for a multilingual customer-support widget. It serves a live demo page, an embeddable frontend widget, and a `POST /chat` endpoint backed by `gpt-4o-mini`.

## What is included

- `POST /chat` with `{ "message": "...", "context": "..." }` input and `{ "reply": "..." }` output
- `GET /health` for runtime checks
- Static demo at `/` with live business-context editing and prompt presets
- Embeddable widget at `/static/widget.js`
- Railway / Render / Procfile-ready backend config
- Vercel config for Python deployment

## Environment

```bash
OPENAI_API_KEY=your_openai_api_key_here
ALLOWED_ORIGINS=*
DEMO_MODE=false
```

`DEMO_MODE=true` enables a lightweight fallback reply path when no OpenAI key is configured, which is useful for pitch demos.

## Local run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_api_key_here
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`.

Use Python `3.12` or `3.13` for local and hosted builds. Python `3.14` can force a source build of `pydantic-core` on some machines.

## Docker run

```bash
docker build -t makoa-wave-chatbot-widget .
docker run --rm -p 8000:8000 -e DEMO_MODE=true makoa-wave-chatbot-widget
```

## Curl test

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola, necesito ayuda con una reserva","context":"Business name: Makoa~Wave\nOffers: snorkel tour $89 adult\nCTA: book now"}'
```

## Embed

```html
<script>
window.MAKOA_WAVE_WIDGET_CONFIG = {
  apiBase: "https://your-app.example.com",
  title: "Chat with Makoa~Wave",
  placeholder: "Ask your question...",
  context: "Business name: Makoa~Wave",
  launcherLabel: "Open multilingual support chat"
};
</script>
<script src="https://your-app.example.com/static/widget.js" defer></script>
```

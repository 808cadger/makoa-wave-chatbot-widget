# Makoa~Wave Chatbot Widget

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
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_api_key_here
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`.

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

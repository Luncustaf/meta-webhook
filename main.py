from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import os
import requests

app = FastAPI()

# Environment Variablen
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")


@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Wird von Meta einmalig zur Verifizierung des Webhooks aufgerufen.
    Meta sendet die Parameter mit Punkten im Namen (hub.verify_token etc.).
    Diese müssen manuell ausgelesen werden.
    """
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Forbidden", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Empfängt alle Webhook-Events von Meta (Messages, Button-Klicks etc.)
    Leitet den kompletten Payload unverändert an Zapier weiter.
    """
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            content={"error": "Invalid JSON"},
            status_code=400
        )

    # Weiterleitung an Zapier (Fire-and

import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def enviar_whatsapp_reserva(
    nombre_cliente,
    email,
    servicio,
    precio,
    sucursal,
    turno,
    vehiculo
):
    url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": settings.WHATSAPP_PHONE_NUMBER,  # ej: 543794075761
        "type": "template",
        "template": {
            "name": "reserva_servicio_taller",  # 👈 EXACTO como en Meta
            "language": {"code": "es_AR"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre_cliente},
                        {"type": "text", "text": email},
                        {"type": "text", "text": servicio},
                        {"type": "text", "text": precio},
                        {"type": "text", "text": sucursal},
                        {"type": "text", "text": turno},
                        {"type": "text", "text": vehiculo},
                    ]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        logger.error(f"❌ WhatsApp error: {response.text}")
    else:
        logger.info("✅ WhatsApp reserva enviada")

    return response.json()

def enviar_whatsapp_cancelacion(
    nombre_cliente,
    email,
    servicio,
    sucursal,
    turno,
    vehiculo
):
    url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": settings.WHATSAPP_PHONE_NUMBER,
        "type": "template",
        "template": {
            "name": "reserva_cancelada_taller",
            "language": {"code": "es_AR"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre_cliente},
                        {"type": "text", "text": email},
                        {"type": "text", "text": servicio},
                        {"type": "text", "text": sucursal},
                        {"type": "text", "text": turno},
                        {"type": "text", "text": vehiculo},
                    ]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

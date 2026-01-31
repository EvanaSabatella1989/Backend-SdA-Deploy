import requests
from django.conf import settings

# def enviar_whatsapp_admin(mensaje: str):
#     url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": "543794075761",  # 👈 TU número admin (el que validaste)
#         "type": "text",
#         "text": {
#             "body": mensaje
#         }
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code != 200:
#         print("❌ Error WhatsApp:", response.text)

#     return response.json()

def enviar_whatsapp_admin(nombre, email, mensaje):
    url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": "543794075761",  # admin En Producción (cuando pases la app a live)# ✔️ SÍ se usa siempre el 9# ✔️ Formato correcto:# 549XXXXXXXXX
        "type": "template",
        "template": {
            "name": "nuevo_contacto",
            "language": {"code": "es_AR"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre},
                        {"type": "text", "text": email},
                        {"type": "text", "text": mensaje},
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
    print(response.status_code, response.text)

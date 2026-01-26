import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

#para enviar los correos mediante resend
def enviar_mail_resend(subject, message, destinatarios):
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.FROM_EMAIL,
                "to": destinatarios,
                "subject": subject,
                "text": message,
            },
            timeout=10
        )

        response.raise_for_status()
        logger.info("📧 Mail enviado correctamente por Resend")
    except Exception as e:
        logger.error(f"❌ Error enviando mail por Resend: {e}")

import json
import logging

import requests
from core.config import settings

logger = logging.getLogger(__name__)


class BrevoEmailClient:
    def __init__(self):
        self.sender_email = settings.brevo_sender_email
        self.sender_name = settings.brevo_sender_name
        self.api_key = settings.brevo_api_key
        self.subject = settings.brevo_subject
        self.service_url = settings.brevo_url

    def _create_header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

    def _create_payload(self, rendered_email, send_to):
        res = json.dumps(
            {
                "sender": {"name": self.sender_name, "email": self.sender_email},
                "to": [{"email": email} for email in send_to],
                "subject": self.subject,
                "htmlContent": rendered_email,
            }
        )
        return res

    def send_email(self, rendered_email, send_to) -> int:
        response = requests.request(
            "POST",
            settings.brevo_url,
            headers=self._create_header(),
            data=self._create_payload(rendered_email, send_to),
        )
        if response.status_code == 201:
            logger.info(f"Email successfully sent to {send_to}")

        return response.status_code


email_sender = BrevoEmailClient()

import json

import requests  # type: ignore
from core.config import settings
from core.worker import celery_app
from jinja2 import Template
from services.helpers import get_template_variables


@celery_app.task
def send_email(event_type: str, notification_data: dict) -> None:
    # берем шаблон в зависимости от типа эвента
    with open(f"templates/{event_type}.html", "r") as template:
        template_str = template.read()

    jinja_template = Template(template_str)
    variables = get_template_variables(template_str)

    # в случае массовых сообщений, шлем сообщение на почту всем юзерам
    mass_maling = notification_data.get("mass_mailing")
    if mass_maling:
        # TODO - реализовать логику отправки массовых сообщений
        pass

    users_list = notification_data.get("users")

    if users_list:
        for user in users_list:
            # подготовка данных для рендеринга шаблона
            user_data = {
                template_var: notification_data.get(template_var)
                or user.get(template_var)
                for template_var in variables
            }
            user_data["sender_email"] = settings.brevo_sender_email

            # рендеринг шаблона с подготовленными данными
            rendered_email = jinja_template.render(user_data)

            email_to = user.get("email")

            payload = json.dumps(
                {
                    "sender": {"name": "Sourabh", "email": settings.brevo_sender_email},
                    "to": [{"email": email_to}],
                    "subject": settings.brevo_subject,
                    "htmlContent": rendered_email,
                }
            )
            headers = {
                "accept": "application/json",
                "api-key": settings.brevo_api_key,
                "content-type": "application/json",
            }
            requests.request("POST", settings.brevo_url, headers=headers, data=payload)

            # TODO добавить сохранение в таблицу

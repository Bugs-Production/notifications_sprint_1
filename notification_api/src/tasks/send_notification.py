import logging

from core.config import settings
from core.worker import celery_app
from db.sync_postgres import get_sync_session
from mocked_auth_api.mocked_auth_api import get_user_info
from models.event import ChannelEnum, Event, EventStatusEnum, EventTypesEnum
from services.email_sender import email_sender
from services.exceptions import RenderTemplateError
from services.helpers import get_template, prepare_template_data, render_template

logger = logging.getLogger(__name__)


@celery_app.task
def send_mass_email(event_type: str, notification_data: dict) -> None:
    template_str = get_template(event_type)
    template_data = prepare_template_data(template_str, notification_data)

    try:
        rendered_email = render_template(template_str, template_data)
    except RenderTemplateError as exc:
        logger.warning(exc)
        return

    page = 1
    while True:
        # Запрашиваем данные о клиентах пачками
        users_data = get_user_info(
            {"page": {"size": settings.brevo_send_to_limit, "page": page}}
        )
        if not users_data:
            break
        send_to = [user.get("email") for user in users_data]

        sender_status_code = email_sender.send_email(rendered_email, send_to)

        # сохраняем результат отправки в БД
        session = get_sync_session()
        event = Event(
            type=EventTypesEnum(event_type),
            channel=ChannelEnum.EMAIL,
            send_to=send_to,
            send_from=settings.brevo_sender_email,
            status=(
                EventStatusEnum.SUCCESS
                if sender_status_code == 201
                else EventStatusEnum.FAILED
            ),
            template=rendered_email,
        )
        session.add(event)
        session.commit()
        logger.info("Notification saved to Database")

        page += 1


@celery_app.task
def send_email(event_type: str, notification_data: dict) -> None:
    users_list = notification_data.get("users", [])

    template_str = get_template(event_type)

    for user in users_list:
        send_to = user.get("email")
        template_data = prepare_template_data(template_str, notification_data, user)

        try:
            rendered_email = render_template(template_str, template_data)
        except RenderTemplateError as exc:
            logger.warning(exc)
            return

        sender_status_code = email_sender.send_email(rendered_email, [send_to])

        # сохраняем результат отправки в БД
        session = get_sync_session()
        event = Event(
            type=EventTypesEnum(event_type),
            channel=ChannelEnum.EMAIL,
            send_to=send_to,
            send_from=settings.brevo_sender_email,
            status=(
                EventStatusEnum.SUCCESS
                if sender_status_code == 201
                else EventStatusEnum.FAILED
            ),
            template=rendered_email,
        )
        session.add(event)
        session.commit()
        logger.info("Notification saved to Database")

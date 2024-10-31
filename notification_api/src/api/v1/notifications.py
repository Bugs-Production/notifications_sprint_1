from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from services.exceptions import NotificationNotFound
from services.notification import NotificationService, get_notification_service

router = APIRouter()


@router.post(
    "/",
    response_model=dict,
    summary="Отправка email сообщения",
    description="Отправка email сообщений разных типов, в зависимости от типа нотификации",
)
async def send_notifications(
    event_type: str,
    event: dict,
    event_service: NotificationService = Depends(get_notification_service),
):
    try:
        event_service.send_email_process(event_type=event_type, event_data=event)
        return {"detail": "successes"}
    except NotificationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

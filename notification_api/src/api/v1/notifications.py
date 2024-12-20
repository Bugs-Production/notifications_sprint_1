from api.jwt_access_token import AccessTokenPayload, check_token, security_jwt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from services.exceptions import NotificationNotFoundError
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
    token: AccessTokenPayload = Depends(security_jwt),
    event_service: NotificationService = Depends(get_notification_service),
):
    check_token(token)
    try:
        await event_service.send_email_process(event_type=event_type, event_data=event)
        return {"detail": "success"}
    except NotificationNotFoundError as notification_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(notification_error)
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(validation_error),
        )

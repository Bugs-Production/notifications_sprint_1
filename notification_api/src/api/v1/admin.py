from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from schemas.admin import CreateAdminNotificationSchema
from services.admin import AdminNotificationService, get_admin_notification_service
from services.exceptions import NotificationNotFoundError, ChannelNotFoundError

router = APIRouter()


@router.post(
    "/",
    response_model=dict,
    summary="Создать задачу на рассылку нотификаций",
    description="Создать задачу на отправку сообщений разных типов, в зависимости от типа нотификации",
)
async def send_notifications(
    notification_data: CreateAdminNotificationSchema,
    notification_service: AdminNotificationService = Depends(
        get_admin_notification_service
    ),
):
    try:
        await notification_service.add_notification_task(
            notification_data=notification_data
        )
        return {"detail": "success"}
    except NotificationNotFoundError as notification_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(notification_error)
        )
    except ChannelNotFoundError as notification_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(notification_error)
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(validation_error),
        )

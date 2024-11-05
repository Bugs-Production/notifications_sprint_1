from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from pydantic import ValidationError
from schemas.admin import CreateAdminNotificationSchema, GetAdminNotificationSchema
from services.admin import AdminNotificationService, get_admin_notification_service
from services.exceptions import ChannelNotFoundError, NotificationNotFoundError

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


@router.get(
    "/",
    response_model=Page[GetAdminNotificationSchema],
    summary="Получить задачи на рассылку нотификаций",
    description="Получение списка задач по отправке нотификаций",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера при обработке запроса.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error"}}
            },
        },
    },
)
async def get_notifications(
    notification_service: AdminNotificationService = Depends(
        get_admin_notification_service
    ),
) -> Page[GetAdminNotificationSchema]:
    notifications_list = await notification_service.get_notifications_list()
    return paginate(notifications_list)


@router.delete(
    "/{notification_id}",
    response_model=dict,
    summary="Удалить задачу на рассылку нотификаций",
    description="Удаление задачи на отправку сообщений",
)
async def delete_notifications(
    notification_id: str,
    notification_service: AdminNotificationService = Depends(
        get_admin_notification_service
    ),
):
    try:
        await notification_service.delete_notification_task(
            notification_id=notification_id
        )
        return {"detail": "success"}
    except NotificationNotFoundError as notification_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(notification_error)
        )

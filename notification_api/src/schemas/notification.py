from enum import Enum

from pydantic import BaseModel


class NotificationType(Enum):
    REGISTRATION = "registration"
    MOVIE_RECOMMENDATION = "movies_recommendation"
    LIKE_NOTIFICATION = "likes_reviews"
    PROMOTION = "promotion"


class UserInfo(BaseModel):
    username: str
    lastname: str
    email: str


class BaseEvent(BaseModel):
    mass_mailing: bool
    users: list[UserInfo] | None = []


class RegistrationEvent(BaseEvent):
    confirmation_link: str


class MovieRecommendationEvent(BaseEvent):
    movies: dict


class LikeReviewsEvent(BaseEvent):
    likes_count: int
    post_link: str


class MassEvent(BaseEvent):
    body_header: str
    body_main: str


NOTIFICATION_MAP = {
    NotificationType.REGISTRATION.value: RegistrationEvent,
    NotificationType.MOVIE_RECOMMENDATION.value: MovieRecommendationEvent,
    NotificationType.LIKE_NOTIFICATION.value: LikeReviewsEvent,
    NotificationType.PROMOTION.value: MassEvent,
}

from enum import Enum
from typing import Type

from pydantic import BaseModel


class NotificationType(str, Enum):
    REGISTRATION = "registration"
    MOVIE_RECOMMENDATION = "movies_recommendation"
    LIKE_NOTIFICATION = "likes_reviews"


class BaseEvent(BaseModel):
    username: str
    lastname: str
    email: str
    sender_email: str


class RegistrationEvent(BaseEvent):
    confirmation_link: str


class MovieRecommendationEvent(BaseEvent):
    movies: dict


class LikeReviewsEvent(BaseEvent):
    likes_count: int
    post_link: str


NOTIFICATION_MAP: dict[str, Type[BaseModel]] = {
    NotificationType.REGISTRATION: RegistrationEvent,
    NotificationType.MOVIE_RECOMMENDATION: MovieRecommendationEvent,
    NotificationType.LIKE_NOTIFICATION: LikeReviewsEvent,
}

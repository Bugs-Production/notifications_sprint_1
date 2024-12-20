# mypy: ignore-errors
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    project_name: str = Field("notification_api", alias="PROJECT_NAME")
    broker_url: str = Field("amqp://user:password@rabbitmq:5672/", alias="BROKER_URL")
    postgres_url: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/foo", alias="POSTGRES_URL"
    )
    postgres_sync_url: str = Field(
        "postgresql+psycopg2://postgres:postgres@db:5432/foo", alias="POSTGRES_SYNC_URL"
    )
    engine_echo: bool = Field(default=False, alias="ENGINE_ECHO")
    brevo_api_key: str = Field("your_api_key", alias="BREVO_API_KEY")
    brevo_url: str = Field("//api.brevo.com/v3/smtp/email", alias="BREVO_URL")
    brevo_subject: str = Field("cinema", alias="BREVO_SUBJECT")
    brevo_sender_email: str = Field("example@gmail.com", alias="BREVO_SENDER_EMAIL")
    brevo_sender_name: str = Field("Sender", alias="BREVO_SENDER_NAME")
    brevo_send_to_limit: int = Field(50, alias="BREVO_SEND_TO_LIMIT")
    celery_scheduler_interval_sec: int = Field(
        60, alias="CELERY_SСHEDULER_INTERVAL_SEC"
    )
    celery_max_retries: int = Field(default=3, alias="CELERY_MAX_RETRIES")
    celery_soft_time_limit: int = Field(default=300, alias="CELERY_SOFT_TIME_LIMIT")
    celery_hard_time_limit: int = Field(default=600, alias="CELERY_HARD_TIME_LIMIT")
    jwt_secret_key: str = Field("my_secret_key", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("my_jwt_algorithm", alias="JWT_ALGORITHM")


settings = Settings()

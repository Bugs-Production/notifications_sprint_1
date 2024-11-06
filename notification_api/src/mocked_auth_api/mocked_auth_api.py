from faker import Faker
from pydantic import BaseModel

fake = Faker()


class User(BaseModel):
    username: str
    lastname: str
    email: str


def get_user_info() -> list[dict]:
    return [
        User(
            username=fake.first_name(), lastname=fake.last_name(), email=fake.email()
        ).model_dump()
        for _ in range(10)
    ]

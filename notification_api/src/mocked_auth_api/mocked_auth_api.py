from faker import Faker
from pydantic import BaseModel

fake = Faker()


class User(BaseModel):
    username: str
    lastname: str
    email: str


def get_user_info(filter: dict) -> list[dict]:
    users_result = [
        User(
            username=fake.first_name(), lastname=fake.last_name(), email=fake.email()
        ).model_dump()
        for _ in range(10)
    ]
    if "page" in filter:
        # Запросы от nofification API будут забирать информацию о клиентах пачками.
        # Например filter = {"page": {"size": 5, "page": 1}}
        # Для упрощения, будем возвращать результат делать ориентируясь только на 'size'

        size = filter["page"]["size"]
        page = filter["page"]["page"]
        if page == 5:
            # Замоканый вариант, когда данные о пользователях закончились и возвращаем пустой список
            return []
        users_result = [
            User(
                username=fake.first_name(), lastname=fake.last_name(), email=fake.email()
            ).model_dump()
            for _ in range(size)
        ]

    return users_result

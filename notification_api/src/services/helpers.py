from jinja2 import Environment, meta


def get_template_variables(template: str) -> set:
    """Для получения переменных в шаблоне."""

    # Создаем Jinja2 окружение
    env = Environment()

    # Парсим шаблон в AST
    parsed_content = env.parse(template)

    # Получаем список переменных
    return meta.find_undeclared_variables(parsed_content)

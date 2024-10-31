from jinja2 import Environment, meta


def get_template_variables(template: str) -> set:
    """Для получения переменных в шаблоне."""
    env = Environment()
    parsed_content = env.parse(template)
    return meta.find_undeclared_variables(parsed_content)

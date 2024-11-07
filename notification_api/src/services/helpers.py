import logging
from pathlib import Path

from core.config import settings
from jinja2 import Environment, Template, meta
from services.exceptions import RenderTemplateError

logger = logging.getLogger(__name__)

templates_dir = Path("templates")


def get_template_variables(template: str) -> set:
    """Для получения переменных в шаблоне."""
    env = Environment()
    parsed_content = env.parse(template)
    return meta.find_undeclared_variables(parsed_content)


def get_template(event_type: str) -> str | None:
    # берем шаблон в зависимости от типа эвента
    template_path = templates_dir / f"{event_type}.html"

    if template_path.exists():
        with open(template_path) as template_file:
            return template_file.read()
    else:
        logger.warning(f"Template {template_path} not found")
        return None


def render_template(template_str: str, template_vars: dict) -> str:
    jinja_template = Template(template_str)
    template_vars["sender_email"] = settings.brevo_sender_email
    rendered_email = jinja_template.render(template_vars)

    if not rendered_email:
        raise RenderTemplateError("Failed to render email")

    return rendered_email


def prepare_template_data(
    template_str: str, notification_data: dict, user_data: dict = None
) -> dict:
    variables = get_template_variables(template_str)
    return {
        template_var: (
            notification_data.get(template_var) or user_data.get(template_var)
            if user_data
            else None
        )
        for template_var in variables
    }

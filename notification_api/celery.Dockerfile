FROM python:3.11

WORKDIR notification_api/src

COPY requirements.txt /notification_api/requirements.txt

RUN pip install --no-cache-dir -r /notification_api/requirements.txt

COPY src /notification_api/src

CMD ["celery", "-A", "main.celery_app", "worker", "--loglevel=info"]
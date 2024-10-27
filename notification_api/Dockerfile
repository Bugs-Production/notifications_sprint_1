FROM python:3.11

WORKDIR notification_api/src

COPY requirements.txt /notification_api/requirements.txt

RUN pip install --no-cache-dir -r /notification_api/requirements.txt

COPY src /notification_api/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

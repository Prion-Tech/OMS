FROM python:3.11-slim

WORKDIR /code/app
COPY ./app/requirements.txt /code/app

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY ./app /code/app

ENV PYTHONPATH=/code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "error"]

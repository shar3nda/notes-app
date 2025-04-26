FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y curl vim && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src
COPY ./alembic.ini /app/alembic.ini

CMD ["uvicorn", "src.main:app", "--log-config", "src/log_conf.yaml", "--host", "0.0.0.0", "--workers", "1"]
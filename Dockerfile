FROM python:3.12-slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--log-config", "src/log_conf.yaml", "--host", "0.0.0.0", "--workers", "1"]
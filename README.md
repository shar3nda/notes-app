# Приложение для заметок

## Пререквизиты

- Python 3.12
- Node.js 22
- Docker

## Установка

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
```

## Запуск бэкенда

### Локально

```sh
dev/start-db.sh
alembic upgrade head
python3 -m src.scripts.seed
```

```sh
uvicorn src.main:app --reload --log-config src/log_conf.yaml
```

### Локально - Docker Compose

```sh
docker compose up -d --build
alembic upgrade head
python3 -m src.scripts.seed
```

## Запуск фронтэнда

```sh
cd frontend
npm run dev
```

Тестовый пользователь:

`user1`

`password1`

FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настройка poetry
ENV POETRY_VERSION=2.1.1 \
    POETRY_HOME=/opt/poetry

# Установка poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && poetry config --system virtualenvs.create false

# Копирование файлов зависимостей
COPY poetry.lock pyproject.toml ./

# Установка зависимостей
RUN poetry install --only=main --sync

# Копирование кода приложения
COPY ..

# Открываем порт для доступа к приложению
EXPOSE 8000


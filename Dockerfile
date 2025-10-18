# Простой single-stage Dockerfile для Bot и API
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Установка uv для управления зависимостями
RUN pip install --no-cache-dir uv

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей через uv
RUN uv sync

# Копирование исходного кода
COPY src/ ./src/
COPY migrations/ ./migrations/

# Порт для API сервиса
EXPOSE 8000

# CMD определяется в docker-compose для каждого сервиса


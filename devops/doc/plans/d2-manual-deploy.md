# План Спринта D2 - Развертывание на сервер

## Обзор

Развернуть приложение на удаленном production сервере вручную по пошаговой инструкции, используя готовые Docker образы из GitHub Container Registry.

## Параметры сервера

- **Адрес:** 83.147.246.172
- **Пользователь:** systech
- **Рабочая директория:** `/opt/systech/pyvovar`
- **Порты:** 3007 (frontend), 8007 (api)
- **Docker образы:**
  - `ghcr.io/eugene-d-evelop/systech-aidd-api:latest`
  - `ghcr.io/eugene-d-evelop/systech-aidd-bot:latest`
  - `ghcr.io/eugene-d-evelop/systech-aidd-frontend:latest`

## Этапы реализации

### 1. Обновить docker-compose.prod.yml

**Файл:** `docker-compose.prod.yml`

Изменить маппинг портов для production:
- Frontend: `3007:3000` (внешний порт 3007)
- API: `8007:8000` (внешний порт 8007)
- Обновить `NEXT_PUBLIC_API_URL` на `http://83.147.246.172:8007`
- Убедиться что образы указывают на `ghcr.io/eugene-d-evelop/systech-aidd-*:latest`

### 2. Создать шаблон .env.production

**Файл:** `.env.production`

Создать подробный шаблон со всеми переменными окружения:

```env
# ===========================================
# TELEGRAM BOT CONFIGURATION
# ===========================================
TELEGRAM_BOT_TOKEN=<your_bot_token_from_BotFather>

# ===========================================
# OPENROUTER API CONFIGURATION
# ===========================================
OPENROUTER_API_KEY=<your_openrouter_api_key>
OPENROUTER_MODEL=openai/gpt-4o-mini

# ===========================================
# LLM PARAMETERS
# ===========================================
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=60

# ===========================================
# BOT SETTINGS
# ===========================================
SYSTEM_PROMPT=Ты полезный AI-ассистент. Отвечай кратко и по существу.
MAX_HISTORY_LENGTH=10

# ===========================================
# DATABASE CONFIGURATION
# ===========================================
DATABASE_URL=postgresql://postgres:SecurePassword123!@postgres:5432/systech_aidd
DATABASE_TIMEOUT=10

# ===========================================
# POSTGRES CREDENTIALS
# ===========================================
POSTGRES_DB=systech_aidd
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SecurePassword123!
```

С комментариями и описанием каждой секции.

### 3. Создать скрипт проверки работоспособности

**Файл:** `deploy-check.sh`

Создать bash-скрипт для автоматической проверки всех сервисов:

```bash
#!/bin/bash
# Проверка работоспособности развернутых сервисов
# - API health endpoint
# - Frontend доступность
# - Docker containers статус
# - PostgreSQL подключение
# - Логи на ошибки
```

Скрипт должен:
- Проверять доступность API (http://83.147.246.172:8007/health)
- Проверять доступность Frontend (http://83.147.246.172:3007)
- Проверять статус всех контейнеров
- Выводить последние логи каждого сервиса
- Возвращать exit code 0 при успехе, 1 при ошибке

### 4. Создать инструкцию по деплою

**Файл:** `docs/guides/manual-deploy.md`

Создать детальную пошаговую инструкцию, включающую:

#### 4.1. Подготовка
- Проверка наличия SSH ключа
- Проверка наличия файлов: `docker-compose.prod.yml`, `.env`
- Список необходимых команд и инструментов

#### 4.2. SSH подключение
- Команды для подключения с использованием SSH ключа
- Проверка версий Docker и Docker Compose на сервере
- Создание рабочей директории `/opt/systech/pyvovar`

#### 4.3. Копирование файлов
- Копирование `docker-compose.prod.yml` через `scp`
- Копирование `.env` через `scp`
- Копирование файлов миграций `migrations/*.sql`
- Проверка прав доступа к файлам

#### 4.4. Загрузка образов
- Pull образов из ghcr.io (bot, api, frontend)
- Проверка загруженных образов (`docker images`)

#### 4.5. Запуск сервисов
- Запуск через `docker-compose -f docker-compose.prod.yml up -d`
- Проверка статуса контейнеров (`docker-compose ps`)
- Просмотр логов для каждого сервиса

#### 4.6. Применение миграций
- Подключение к контейнеру API
- Запуск миграций: `docker exec <container> uv run python -m src.migrations`
- Проверка таблиц в PostgreSQL

#### 4.7. Проверка работоспособности
- Health check API: `curl http://83.147.246.172:8007/health`
- Проверка Frontend: `curl http://83.147.246.172:3007`
- Проверка логов всех сервисов
- Тестирование Telegram бота
- Тестирование API endpoints

#### 4.8. Troubleshooting
- Типичные проблемы и их решения
- Команды для диагностики
- Перезапуск сервисов

### 5. Выполнить деплой на сервер

Пройти по инструкции `docs/guides/manual-deploy.md` шаг за шагом:

1. Подключиться к серверу по SSH
2. Создать директорию `/opt/systech/pyvovar`
3. Скопировать необходимые файлы
4. Загрузить Docker образы
5. Запустить сервисы
6. Применить миграции
7. Проверить работоспособность

### 6. Создать отчет о развертывании

**Файл:** `devops/doc/reports/d2-deployment-report.md`

Задокументировать процесс развертывания:
- Скриншоты/логи успешного запуска
- Результаты проверок (curl, logs)
- Подтверждение работы всех сервисов
- Ссылки на работающие сервисы
- Проблемы и их решения (если были)

### 7. Обновить документацию

**Файл:** `devops/doc/devops-roadmap.md`

- Изменить статус D2 на "✅ Done"
- Добавить ссылку на план: `[План](plans/d2-manual-deploy.md)`

**Файл:** `README.md` (опционально)

- Добавить секцию "🌐 Production Deployment" с ссылками на работающие сервисы

## Ключевые файлы

### Новые файлы:
- `docs/guides/manual-deploy.md` - детальная инструкция по деплою
- `.env.production` - шаблон конфигурации для production
- `deploy-check.sh` - скрипт проверки работоспособности
- `devops/doc/plans/d2-manual-deploy.md` - этот план
- `devops/doc/reports/d2-deployment-report.md` - отчет о развертывании

### Изменяемые файлы:
- `docker-compose.prod.yml` - обновить порты и URL
- `devops/doc/devops-roadmap.md` - обновить статус D2

## Что НЕ делаем (MVP подход)

- ❌ Автоматизация деплоя (будет в D3)
- ❌ CI/CD для автоматического обновления
- ❌ SSL/HTTPS сертификаты (nginx, certbot)
- ❌ Мониторинг (Prometheus, Grafana)
- ❌ Backup и restore процедуры
- ❌ Blue-green deployment
- ❌ Health checks в docker-compose
- ❌ Restart policies (оставляем unless-stopped)

## Критерии успеха

- ✅ Инструкция `manual-deploy.md` создана и детальная
- ✅ Все файлы скопированы на сервер
- ✅ Docker образы успешно загружены из ghcr.io
- ✅ Все 4 сервиса (postgres, bot, api, frontend) запущены
- ✅ Миграции БД применены успешно
- ✅ API доступен по адресу http://83.147.246.172:8007
- ✅ Frontend доступен по адресу http://83.147.246.172:3007
- ✅ Telegram Bot отвечает на сообщения
- ✅ Отчет о развертывании создан
- ✅ Документация обновлена


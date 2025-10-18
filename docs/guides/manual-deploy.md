# Руководство по ручному развертыванию на production сервере

## Обзор

Данное руководство описывает процесс ручного развертывания приложения systech-aidd на production сервере с использованием Docker образов из GitHub Container Registry.

**Время выполнения:** ~30 минут  
**Уровень сложности:** Средний

## Параметры сервера

- **Адрес:** 83.147.246.172
- **Пользователь:** systech
- **Рабочая директория:** `/opt/systech/pyvovar`
- **Порты:**
  - Frontend: 3007
  - API: 8007
  - PostgreSQL: 5432 (внутренний)

## Требования

### Локально (ваш компьютер)

- SSH клиент
- SSH ключ для доступа к серверу
- Git (для клонирования репозитория, опционально)

### На сервере

✅ Docker (установлен)  
✅ Docker Compose (установлен)  
✅ SSH доступ с ключом (настроен)

---

## Шаг 1. Подготовка локально

### 1.1. Проверка SSH ключа

Убедитесь, что у вас есть SSH ключ для подключения к серверу:

```bash
# Проверка наличия SSH ключа
ls -la ~/.ssh/

# Должны быть файлы:
# - id_rsa или другой приватный ключ
# - id_rsa.pub или другой публичный ключ
```

Если ключ предоставлен отдельно, сохраните его:

```bash
# Сохраните ключ в ~/.ssh/systech_server
# Установите правильные права
chmod 600 ~/.ssh/systech_server
```

### 1.2. Проверка наличия необходимых файлов

Убедитесь, что у вас есть следующие файлы в корне проекта:

- ✅ `docker-compose.prod.yml` - конфигурация для production
- ✅ `.env` - файл с переменными окружения (или создайте из `env.production.example`)
- ✅ `migrations/*.sql` - SQL файлы миграций

```bash
# Проверка наличия файлов
ls -la docker-compose.prod.yml
ls -la .env  # или создайте: cp env.production.example .env
ls -la migrations/*.sql
```

### 1.3. Подготовка .env файла

Если у вас нет `.env` файла, создайте его:

```bash
# Скопируйте шаблон
cp env.production.example .env

# Отредактируйте и заполните реальными значениями
nano .env  # или используйте другой редактор
```

**Обязательно заполните:**
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `OPENROUTER_API_KEY` - API ключ от OpenRouter
- `POSTGRES_PASSWORD` - сильный пароль для PostgreSQL

---

## Шаг 2. SSH подключение к серверу

### 2.1. Подключение

Подключитесь к серверу по SSH:

```bash
# Если используете стандартный SSH ключ (~/.ssh/id_rsa)
ssh systech@83.147.246.172

# Если используете отдельный ключ
ssh -i ~/.ssh/systech_server systech@83.147.246.172
```

### 2.2. Проверка версий Docker

После подключения проверьте установленные версии:

```bash
# Версия Docker
docker --version
# Ожидается: Docker version 20.10.x или выше

# Версия Docker Compose
docker-compose --version
# Ожидается: Docker Compose version 2.x.x или выше
```

### 2.3. Создание рабочей директории

Создайте директорию для проекта:

```bash
# Создание директории
sudo mkdir -p /opt/systech/pyvovar

# Смена владельца
sudo chown -R systech:systech /opt/systech/pyvovar

# Переход в рабочую директорию
cd /opt/systech/pyvovar

# Проверка
pwd
# Ожидается: /opt/systech/pyvovar
```

---

## Шаг 3. Копирование файлов на сервер

**Откройте НОВОЕ окно терминала** на вашем локальном компьютере (не закрывая SSH сессию).

### 3.1. Копирование docker-compose.prod.yml

```bash
# Перейдите в директорию проекта локально
cd /path/to/systech-aidd

# Копирование docker-compose файла
scp docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/

# Если используете отдельный ключ:
scp -i ~/.ssh/systech_server docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/
```

### 3.2. Копирование .env файла

```bash
# ВАЖНО: Убедитесь, что .env содержит реальные секреты!
scp .env systech@83.147.246.172:/opt/systech/pyvovar/

# Если используете отдельный ключ:
scp -i ~/.ssh/systech_server .env systech@83.147.246.172:/opt/systech/pyvovar/
```

### 3.3. Копирование файлов миграций

```bash
# Создание директории migrations на сервере
ssh systech@83.147.246.172 "mkdir -p /opt/systech/pyvovar/migrations"

# Копирование всех SQL файлов
scp migrations/*.sql systech@83.147.246.172:/opt/systech/pyvovar/migrations/

# Если используете отдельный ключ:
scp -i ~/.ssh/systech_server migrations/*.sql systech@83.147.246.172:/opt/systech/pyvovar/migrations/
```

### 3.4. Проверка скопированных файлов

**Вернитесь в окно SSH сессии** на сервере:

```bash
# Проверка наличия файлов
cd /opt/systech/pyvovar
ls -la

# Должны быть:
# - docker-compose.prod.yml
# - .env
# - migrations/ (директория с SQL файлами)

# Проверка миграций
ls -la migrations/
# Должны быть: 001_create_messages.sql, 002_create_users.sql, 003_create_chat_messages.sql
```

### 3.5. Проверка прав доступа

```bash
# Проверка владельца
ls -la /opt/systech/pyvovar

# Если нужно, измените владельца
sudo chown -R systech:systech /opt/systech/pyvovar

# Проверка .env файла (должен быть приватным)
chmod 600 .env
```

---

## Шаг 4. Загрузка Docker образов

### 4.1. Pull образов из GitHub Container Registry

Образы публично доступны, авторизация не требуется:

```bash
# Переход в рабочую директорию
cd /opt/systech/pyvovar

# Загрузка всех образов
docker-compose -f docker-compose.prod.yml pull

# Ожидаемый вывод:
# Pulling postgres  ... done
# Pulling bot       ... done
# Pulling api       ... done
# Pulling frontend  ... done
```

### 4.2. Проверка загруженных образов

```bash
# Просмотр загруженных образов
docker images | grep systech-aidd

# Ожидаемые образы:
# ghcr.io/eugene-d-evelop/systech-aidd-api
# ghcr.io/eugene-d-evelop/systech-aidd-bot
# ghcr.io/eugene-d-evelop/systech-aidd-frontend
# postgres:16-alpine
```

---

## Шаг 5. Запуск сервисов

### 5.1. Запуск в фоновом режиме

```bash
# Запуск всех сервисов
docker-compose -f docker-compose.prod.yml up -d

# Ожидаемый вывод:
# Creating network "pyvovar_default" done
# Creating volume "pyvovar_postgres_data" done
# Creating pyvovar_postgres_1 ... done
# Creating pyvovar_bot_1      ... done
# Creating pyvovar_api_1      ... done
# Creating pyvovar_frontend_1 ... done
```

### 5.2. Проверка статуса контейнеров

```bash
# Просмотр запущенных контейнеров
docker-compose -f docker-compose.prod.yml ps

# Ожидаемый вывод:
# NAME                 STATUS          PORTS
# pyvovar_postgres_1   Up X seconds    0.0.0.0:5432->5432/tcp
# pyvovar_bot_1        Up X seconds    
# pyvovar_api_1        Up X seconds    0.0.0.0:8007->8000/tcp
# pyvovar_frontend_1   Up X seconds    0.0.0.0:3007->3000/tcp
```

Все контейнеры должны быть в статусе `Up`.

### 5.3. Просмотр логов

```bash
# Логи всех сервисов
docker-compose -f docker-compose.prod.yml logs

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs api
docker-compose -f docker-compose.prod.yml logs bot
docker-compose -f docker-compose.prod.yml logs frontend

# Логи в режиме follow (ctrl+c для выхода)
docker-compose -f docker-compose.prod.yml logs -f api
```

**Что искать в логах:**
- ✅ PostgreSQL: `database system is ready to accept connections`
- ✅ API: `Uvicorn running on http://0.0.0.0:8000`
- ✅ Bot: `Start polling` или `Bot initialized`
- ✅ Frontend: `Local: http://localhost:3000`

---

## Шаг 6. Применение миграций базы данных

### 6.1. Найти имя контейнера API

```bash
# Получить имя контейнера API
docker ps --filter "name=api" --format "{{.Names}}"

# Или использовать docker-compose
CONTAINER_NAME=$(docker-compose -f docker-compose.prod.yml ps -q api)
```

### 6.2. Запуск миграций

```bash
# Вариант 1: Используя имя контейнера напрямую
docker exec pyvovar_api_1 uv run python -m src.migrations

# Вариант 2: Используя docker-compose exec
docker-compose -f docker-compose.prod.yml exec api uv run python -m src.migrations
```

**Ожидаемый вывод:**

```
INFO - Found 3 migration file(s)
INFO - Running migration: 001_create_messages.sql
INFO - Migration 001_create_messages.sql completed successfully
INFO - Running migration: 002_create_users.sql
INFO - Migration 002_create_users.sql completed successfully
INFO - Running migration: 003_create_chat_messages.sql
INFO - Migration 003_create_chat_messages.sql completed successfully
INFO - All migrations completed successfully
```

### 6.3. Проверка таблиц в PostgreSQL

```bash
# Подключение к PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d systech_aidd

# В psql выполните:
\dt

# Ожидаемые таблицы:
# messages
# users
# chat_messages

# Выход из psql
\q
```

---

## Шаг 7. Проверка работоспособности

### 7.1. Health Check API

```bash
# На сервере или локально
curl http://83.147.246.172:8007/health

# Ожидаемый ответ:
# {"status":"healthy"}
```

### 7.2. Проверка API Documentation

```bash
# Проверка Swagger UI
curl http://83.147.246.172:8007/docs

# Ожидаемый ответ: HTML страница с документацией
```

**Или откройте в браузере:**
- http://83.147.246.172:8007/docs - Swagger UI

### 7.3. Проверка Frontend

```bash
# Проверка доступности Frontend
curl http://83.147.246.172:3007

# Ожидаемый ответ: HTML страница Next.js приложения
```

**Или откройте в браузере:**
- http://83.147.246.172:3007 - Frontend приложения
- http://83.147.246.172:3007/dashboard - Dashboard страница

### 7.4. Проверка логов на ошибки

```bash
# Проверка последних логов API
docker-compose -f docker-compose.prod.yml logs --tail=50 api | grep -i error

# Проверка последних логов Bot
docker-compose -f docker-compose.prod.yml logs --tail=50 bot | grep -i error

# Если ошибок нет - все работает корректно
```

### 7.5. Тестирование Telegram бота

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте команду `/start`
4. Бот должен ответить приветственным сообщением

### 7.6. Тестирование API endpoints

```bash
# Получение статистики dashboard
curl http://83.147.246.172:8007/api/stats/dashboard

# Отправка сообщения в чат (опционально)
curl -X POST http://83.147.246.172:8007/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Привет!",
    "session_id": "test-123",
    "mode": "normal"
  }'
```

### 7.7. Автоматическая проверка (опционально)

Если вы скопировали скрипт `deploy-check.sh` на сервер:

```bash
# Запуск скрипта проверки
bash deploy-check.sh 83.147.246.172

# Или сделайте его исполняемым
chmod +x deploy-check.sh
./deploy-check.sh 83.147.246.172
```

---

## Шаг 8. Управление сервисами

### Остановка сервисов

```bash
# Остановка всех сервисов
docker-compose -f docker-compose.prod.yml stop

# Остановка конкретного сервиса
docker-compose -f docker-compose.prod.yml stop api
```

### Перезапуск сервисов

```bash
# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart api
```

### Остановка и удаление контейнеров

```bash
# Остановка и удаление контейнеров (данные БД сохранятся)
docker-compose -f docker-compose.prod.yml down

# Остановка и удаление контейнеров + volumes (УДАЛИТ ВСЕ ДАННЫЕ!)
docker-compose -f docker-compose.prod.yml down -v
```

### Просмотр логов

```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100

# Follow mode (реального времени)
docker-compose -f docker-compose.prod.yml logs -f

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs -f api
```

### Обновление образов

```bash
# Загрузка новых версий образов
docker-compose -f docker-compose.prod.yml pull

# Пересоздание и запуск контейнеров с новыми образами
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

---

## Troubleshooting

### Проблема: Контейнер не запускается

**Симптомы:**
```bash
docker-compose ps
# Status: Restarting или Exit
```

**Решение:**

1. Проверьте логи контейнера:
```bash
docker-compose -f docker-compose.prod.yml logs <service_name>
```

2. Проверьте .env файл:
```bash
cat .env
# Убедитесь что все переменные заполнены
```

3. Проверьте порты (не заняты ли):
```bash
sudo netstat -tulpn | grep -E ':(3007|8007|5432)'
```

### Проблема: API недоступен извне

**Симптомы:**
```bash
curl http://83.147.246.172:8007/health
# Connection refused или timeout
```

**Решение:**

1. Проверьте firewall:
```bash
# Ubuntu/Debian
sudo ufw status
sudo ufw allow 8007/tcp
sudo ufw allow 3007/tcp

# CentOS/RHEL
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=8007/tcp --permanent
sudo firewall-cmd --add-port=3007/tcp --permanent
sudo firewall-cmd --reload
```

2. Проверьте что API слушает правильный порт:
```bash
docker-compose -f docker-compose.prod.yml exec api netstat -tulpn
```

### Проблема: База данных не подключается

**Симптомы:**
```
ERROR - could not connect to server
```

**Решение:**

1. Проверьте что PostgreSQL запущен:
```bash
docker-compose -f docker-compose.prod.yml ps postgres
```

2. Проверьте пароль в .env:
```bash
grep POSTGRES_PASSWORD .env
grep DATABASE_URL .env
# Пароли должны совпадать!
```

3. Проверьте healthcheck PostgreSQL:
```bash
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres
```

### Проблема: Миграции не применяются

**Симптомы:**
```
ERROR - Migrations directory not found
```

**Решение:**

1. Проверьте наличие файлов миграций:
```bash
ls -la migrations/
```

2. Скопируйте миграции в контейнер вручную:
```bash
docker cp migrations/ pyvovar_api_1:/app/migrations/
```

3. Повторите применение миграций:
```bash
docker-compose -f docker-compose.prod.yml exec api uv run python -m src.migrations
```

### Проблема: Frontend показывает ошибку подключения к API

**Симптомы:**
```
Failed to fetch
Network Error
```

**Решение:**

1. Проверьте NEXT_PUBLIC_API_URL в docker-compose.prod.yml:
```bash
grep NEXT_PUBLIC_API_URL docker-compose.prod.yml
# Должно быть: http://83.147.246.172:8007
```

2. Пересоздайте frontend контейнер:
```bash
docker-compose -f docker-compose.prod.yml up -d --force-recreate frontend
```

### Проблема: Telegram Bot не отвечает

**Симптомы:**
- Бот не отвечает на сообщения

**Решение:**

1. Проверьте логи бота:
```bash
docker-compose -f docker-compose.prod.yml logs bot | tail -50
```

2. Проверьте токен в .env:
```bash
grep TELEGRAM_BOT_TOKEN .env
```

3. Проверьте что бот может подключиться к Telegram API:
```bash
docker-compose -f docker-compose.prod.yml exec bot curl https://api.telegram.org
```

4. Перезапустите бота:
```bash
docker-compose -f docker-compose.prod.yml restart bot
```

---

## Полезные команды

### Мониторинг ресурсов

```bash
# Использование ресурсов контейнерами
docker stats

# Размер образов
docker images | grep systech-aidd

# Использование дисков
df -h

# Логи systemd (если docker запущен через systemd)
sudo journalctl -u docker -f
```

### Очистка

```bash
# Удаление неиспользуемых образов
docker image prune -a

# Удаление неиспользуемых volumes
docker volume prune

# Полная очистка (ОСТОРОЖНО!)
docker system prune -a --volumes
```

### Бэкап базы данных

```bash
# Создание бэкапа
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres systech_aidd > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление из бэкапа
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres systech_aidd < backup_20241018_120000.sql
```

---

## Следующие шаги

После успешного развертывания:

1. ✅ **Настройте регулярные бэкапы БД** (cron job)
2. ✅ **Настройте мониторинг** (логи, алерты)
3. ✅ **Документируйте процесс обновления**
4. ✅ **Подготовьте к Спринту D3** (автоматизация деплоя)

---

## Контакты и поддержка

- **Документация проекта:** `/docs`
- **DevOps роадмап:** `devops/doc/devops-roadmap.md`
- **План спринта D2:** `devops/doc/plans/d2-manual-deploy.md`

---

**Поздравляем! 🎉**

Приложение успешно развернуто на production сервере!

- Frontend: http://83.147.246.172:3007
- API: http://83.147.246.172:8007
- API Docs: http://83.147.246.172:8007/docs


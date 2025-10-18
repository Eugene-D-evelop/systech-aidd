# 🚀 Команды для развертывания (копи-паста)

## Быстрая справка для деплоя на 83.147.246.172

---

## 1️⃣ ПОДГОТОВКА (локально)

```bash
# Создать .env файл
cp env.production.example .env
nano .env  # ВАЖНО: заполните реальные токены!

# Проверить файлы
ls -la docker-compose.prod.yml .env migrations/

# Тест SSH подключения
ssh systech@83.147.246.172
```

---

## 2️⃣ КОПИРОВАНИЕ ФАЙЛОВ (локально)

```bash
# Копирование docker-compose
scp docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/

# Копирование .env
scp .env systech@83.147.246.172:/opt/systech/pyvovar/

# Копирование миграций
ssh systech@83.147.246.172 "mkdir -p /opt/systech/pyvovar/migrations"
scp migrations/*.sql systech@83.147.246.172:/opt/systech/pyvovar/migrations/

# Копирование скрипта проверки (опционально)
scp deploy-check.sh systech@83.147.246.172:/opt/systech/pyvovar/
```

---

## 3️⃣ РАЗВЕРТЫВАНИЕ (на сервере)

```bash
# Подключение к серверу
ssh systech@83.147.246.172

# Переход в рабочую директорию
cd /opt/systech/pyvovar

# Проверка файлов
ls -la

# Загрузка Docker образов
docker-compose -f docker-compose.prod.yml pull

# Запуск сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Применение миграций
docker-compose -f docker-compose.prod.yml exec api uv run python -m src.migrations
```

---

## 4️⃣ ПРОВЕРКА (на сервере)

```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# API health check
curl http://83.147.246.172:8007/health

# Frontend check
curl http://83.147.246.172:3007

# Логи сервисов
docker-compose -f docker-compose.prod.yml logs --tail=50

# Автоматическая проверка
bash deploy-check.sh 83.147.246.172
```

---

## 5️⃣ ПОЛЕЗНЫЕ КОМАНДЫ

```bash
# Просмотр логов в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f bot
docker-compose -f docker-compose.prod.yml logs -f frontend

# Перезапуск сервиса
docker-compose -f docker-compose.prod.yml restart api

# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Остановка сервисов
docker-compose -f docker-compose.prod.yml stop

# Остановка и удаление (данные БД сохранятся)
docker-compose -f docker-compose.prod.yml down
```

---

## 🆘 TROUBLESHOOTING

```bash
# Проверка портов
sudo netstat -tulpn | grep -E ':(3007|8007)'

# Firewall (если нужно)
sudo ufw allow 8007/tcp
sudo ufw allow 3007/tcp

# Проверка PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres

# Повторное применение миграций
docker-compose -f docker-compose.prod.yml exec api uv run python -m src.migrations

# Пересоздание контейнеров
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

---

## 📊 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ

### API Health Check:
```bash
curl http://83.147.246.172:8007/health
# Ответ: {"status":"healthy"}
```

### Docker PS:
```
NAME                 STATUS          PORTS
pyvovar_postgres_1   Up X seconds    0.0.0.0:5432->5432/tcp
pyvovar_bot_1        Up X seconds    
pyvovar_api_1        Up X seconds    0.0.0.0:8007->8000/tcp
pyvovar_frontend_1   Up X seconds    0.0.0.0:3007->3000/tcp
```

### Миграции:
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

---

## 🌐 ССЫЛКИ ПОСЛЕ ДЕПЛОЯ

- **Frontend:** http://83.147.246.172:3007
- **API:** http://83.147.246.172:8007
- **API Docs:** http://83.147.246.172:8007/docs
- **Dashboard:** http://83.147.246.172:3007/dashboard

---

📖 **Полная инструкция:** `docs/guides/manual-deploy.md`


# ✅ Чек-лист готовности к развертыванию

## Статус: ГОТОВ К ДЕПЛОЮ 🚀

Последняя проверка: 18 октября 2025

---

## 1. ✅ Файлы проекта

### Конфигурационные файлы
- ✅ `docker-compose.prod.yml` - **ГОТОВ**
  - Порты: 3007 (frontend), 8007 (api) ✓
  - URL: http://83.147.246.172:8007 ✓
  - Образы: ghcr.io/eugene-d-evelop/systech-aidd-* ✓

- ✅ `env.production.example` - **ГОТОВ**
  - Все переменные описаны ✓
  - Подробные комментарии ✓
  - Production notes ✓

### Миграции базы данных
- ✅ `migrations/001_create_messages.sql` - **ГОТОВ**
- ✅ `migrations/002_create_users.sql` - **ГОТОВ**
- ✅ `migrations/003_create_chat_messages.sql` - **ГОТОВ**

### Документация
- ✅ `docs/guides/manual-deploy.md` - **ГОТОВ**
  - 8 шагов развертывания ✓
  - Troubleshooting секция ✓
  - Полезные команды ✓

- ✅ `devops/doc/DEPLOY_QUICKSTART.md` - **ГОТОВ**
  - Краткая инструкция ✓

- ✅ `devops/FILES_TO_DEPLOY.md` - **ГОТОВ**
  - Список файлов ✓
  - Команды копирования ✓

### Скрипты
- ✅ `deploy-check.sh` - **ГОТОВ**
  - Проверка Docker контейнеров ✓
  - Проверка API и Frontend ✓
  - Проверка логов ✓

---

## 2. ✅ Docker образы в ghcr.io

### Проверка доступности (выполнена 18.10.2025)

- ✅ **Bot образ** - ДОСТУПЕН
  ```
  ghcr.io/eugene-d-evelop/systech-aidd-bot:latest
  Platform: linux/amd64
  Status: ✓ Публично доступен
  ```

- ✅ **API образ** - ДОСТУПЕН
  ```
  ghcr.io/eugene-d-evelop/systech-aidd-api:latest
  Platform: linux/amd64
  Status: ✓ Публично доступен
  ```

- ✅ **Frontend образ** - ДОСТУПЕН
  ```
  ghcr.io/eugene-d-evelop/systech-aidd-frontend:latest
  Platform: linux/amd64
  Status: ✓ Публично доступен
  ```

### Команда проверки:
```bash
# Локально можно проверить:
docker manifest inspect ghcr.io/eugene-d-evelop/systech-aidd-bot:latest
docker manifest inspect ghcr.io/eugene-d-evelop/systech-aidd-api:latest
docker manifest inspect ghcr.io/eugene-d-evelop/systech-aidd-frontend:latest
```

---

## 3. ⚠️ ЧТО НУЖНО ПОДГОТОВИТЬ ПЕРЕД ДЕПЛОЕМ

### 3.1. Создать .env файл
```bash
# Скопируйте шаблон
cp env.production.example .env

# Отредактируйте и заполните:
nano .env
```

**Обязательные переменные для заполнения:**
- [ ] `TELEGRAM_BOT_TOKEN` - токен от @BotFather
- [ ] `OPENROUTER_API_KEY` - API ключ от OpenRouter
- [ ] `POSTGRES_PASSWORD` - сильный пароль для БД
- [ ] `DATABASE_URL` - обновите пароль в URL (должен совпадать с POSTGRES_PASSWORD)

### 3.2. Проверить SSH ключ
```bash
# Проверка наличия ключа
ls -la ~/.ssh/

# Если ключ предоставлен отдельно, сохраните:
# ~/.ssh/systech_server
chmod 600 ~/.ssh/systech_server
```

### 3.3. Проверить SSH подключение
```bash
# Тест подключения
ssh systech@83.147.246.172

# Или с отдельным ключом:
ssh -i ~/.ssh/systech_server systech@83.147.246.172
```

---

## 4. 📋 ИНСТРУКЦИИ ПО РАЗВЕРТЫВАНИЮ

### Детальная инструкция (рекомендуется)
📖 **[docs/guides/manual-deploy.md](../docs/guides/manual-deploy.md)**
- Пошаговое руководство (8 шагов)
- Объяснение каждой команды
- Troubleshooting

### Быстрая инструкция (для опытных)
⚡ **[devops/doc/DEPLOY_QUICKSTART.md](doc/DEPLOY_QUICKSTART.md)**
- Только команды
- Без детальных объяснений

---

## 5. 🎯 ПАРАМЕТРЫ СЕРВЕРА

```
Адрес:            83.147.246.172
Пользователь:     systech
Рабочая директория: /opt/systech/pyvovar

Порты:
- Frontend:       3007  →  http://83.147.246.172:3007
- API:            8007  →  http://83.147.246.172:8007
- API Docs:       8007  →  http://83.147.246.172:8007/docs
- PostgreSQL:     5432  (внутренний, не открыт наружу)

Docker установлен:         ✓
Docker Compose установлен: ✓
SSH доступ настроен:       ✓
```

---

## 6. 📦 СПИСОК ФАЙЛОВ ДЛЯ КОПИРОВАНИЯ

Перед развертыванием подготовьте эти файлы:

**Обязательные:**
1. `docker-compose.prod.yml` ✓
2. `.env` (создайте из env.production.example) ⚠️
3. `migrations/*.sql` (3 файла) ✓

**Опциональные:**
4. `deploy-check.sh` ✓

**Команды копирования:**
```bash
scp docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/
scp .env systech@83.147.246.172:/opt/systech/pyvovar/
scp -r migrations systech@83.147.246.172:/opt/systech/pyvovar/
scp deploy-check.sh systech@83.147.246.172:/opt/systech/pyvovar/
```

---

## 7. ✅ КРИТЕРИИ УСПЕШНОГО ДЕПЛОЯ

После развертывания проверьте:

### Контейнеры
- [ ] PostgreSQL запущен и healthy
- [ ] Bot запущен
- [ ] API запущен
- [ ] Frontend запущен

### Миграции
- [ ] Все 3 миграции применены успешно
- [ ] Таблицы созданы в PostgreSQL (messages, users, chat_messages)

### Доступность сервисов
- [ ] API health: `curl http://83.147.246.172:8007/health` → `{"status":"healthy"}`
- [ ] API docs: http://83.147.246.172:8007/docs → Swagger UI открывается
- [ ] Frontend: http://83.147.246.172:3007 → Страница загружается

### Функциональность
- [ ] Telegram бот отвечает на команду `/start`
- [ ] API endpoints работают
- [ ] Frontend подключается к API
- [ ] Нет критичных ошибок в логах

---

## 8. 🔍 АВТОМАТИЧЕСКАЯ ПРОВЕРКА

После развертывания запустите:

```bash
# На сервере или локально
bash deploy-check.sh 83.147.246.172
```

Скрипт проверит:
- ✓ Статус Docker контейнеров
- ✓ Доступность API (health endpoint)
- ✓ Доступность Frontend
- ✓ Логи на наличие ошибок

---

## 9. 📝 ПОСЛЕ УСПЕШНОГО ДЕПЛОЯ

1. **Создать отчет:**
   - Файл: `devops/doc/reports/d2-deployment-report.md`
   - Включить: логи, результаты проверок, проблемы и решения

2. **Обновить roadmap:**
   - Изменить статус D2 на "✅ Done"
   - Файл: `devops/doc/devops-roadmap.md`

3. **Настроить мониторинг:**
   - Отслеживание логов
   - Регулярные бэкапы PostgreSQL
   - Алерты на ошибки

---

## 🚀 ГОТОВЫ К РАЗВЕРТЫВАНИЮ!

**Статус:** ✅ Все файлы готовы, образы доступны, инструкции актуальны

**Следующий шаг:**
1. Создайте `.env` файл из `env.production.example`
2. Заполните реальные токены и пароли
3. Следуйте инструкции: **[docs/guides/manual-deploy.md](../docs/guides/manual-deploy.md)**

---

**Удачи в развертывании! 🎉**

Если возникнут проблемы, обратитесь к секции Troubleshooting в manual-deploy.md


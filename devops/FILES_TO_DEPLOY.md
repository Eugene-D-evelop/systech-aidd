# Файлы для развертывания на сервер

## Список файлов для копирования

Перед развертыванием убедитесь, что у вас подготовлены следующие файлы:

### ✅ Обязательные файлы

1. **`docker-compose.prod.yml`** (корень проекта)
   - Конфигурация Docker Compose для production
   - Порты: 3007 (frontend), 8007 (api)
   - Образы из ghcr.io

2. **`.env`** (корень проекта)
   - Переменные окружения
   - **ВАЖНО:** Заполните реальными значениями!
   - Шаблон: `env.production.example`

3. **`migrations/*.sql`** (директория migrations)
   - `001_create_messages.sql`
   - `002_create_users.sql`
   - `003_create_chat_messages.sql`

### 🔧 Опциональные файлы

4. **`deploy-check.sh`** (корень проекта)
   - Скрипт автоматической проверки работоспособности
   - Использование: `bash deploy-check.sh 83.147.246.172`

## Команды для копирования

### Вариант 1: Через SCP (по одному файлу)

```bash
scp docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/
scp .env systech@83.147.246.172:/opt/systech/pyvovar/
scp -r migrations systech@83.147.246.172:/opt/systech/pyvovar/
scp deploy-check.sh systech@83.147.246.172:/opt/systech/pyvovar/
```

### Вариант 2: Через SCP с SSH ключом

```bash
scp -i ~/.ssh/systech_server docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/
scp -i ~/.ssh/systech_server .env systech@83.147.246.172:/opt/systech/pyvovar/
scp -i ~/.ssh/systech_server -r migrations systech@83.147.246.172:/opt/systech/pyvovar/
scp -i ~/.ssh/systech_server deploy-check.sh systech@83.147.246.172:/opt/systech/pyvovar/
```

### Вариант 3: Через rsync (рекомендуется)

```bash
rsync -avz -e ssh \
  docker-compose.prod.yml \
  .env \
  migrations/ \
  deploy-check.sh \
  systech@83.147.246.172:/opt/systech/pyvovar/
```

## Проверка после копирования

На сервере выполните:

```bash
cd /opt/systech/pyvovar
ls -la

# Должны быть:
# - docker-compose.prod.yml
# - .env
# - migrations/ (директория)
# - deploy-check.sh (опционально)
```

## Что НЕ нужно копировать

❌ Исходный код (`src/`, `frontend/`) - используются Docker образы  
❌ Node modules (`node_modules/`, `__pycache__/`)  
❌ Git история (`.git/`)  
❌ Локальные конфигурации (`docker-compose.yml` для разработки)  
❌ Виртуальные окружения (`.venv/`, `venv/`)

---

📖 **Полная инструкция:** [`docs/guides/manual-deploy.md`](../docs/guides/manual-deploy.md)


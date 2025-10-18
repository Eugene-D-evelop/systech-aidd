# Быстрый старт развертывания

## Краткая инструкция для опытных пользователей

### 1. Подготовка локально

```bash
# Убедитесь что у вас есть .env файл
cp env.production.example .env
nano .env  # заполните реальными значениями
```

### 2. Копирование на сервер

```bash
# Подключение к серверу
ssh systech@83.147.246.172

# Создание рабочей директории
sudo mkdir -p /opt/systech/pyvovar
sudo chown -R systech:systech /opt/systech/pyvovar
cd /opt/systech/pyvovar

# Копирование файлов (в новом терминале локально)
scp docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pyvovar/
scp .env systech@83.147.246.172:/opt/systech/pyvovar/
scp -r migrations systech@83.147.246.172:/opt/systech/pyvovar/
```

### 3. Запуск на сервере

```bash
cd /opt/systech/pyvovar

# Загрузка образов
docker-compose -f docker-compose.prod.yml pull

# Запуск сервисов
docker-compose -f docker-compose.prod.yml up -d

# Применение миграций
docker-compose -f docker-compose.prod.yml exec api uv run python -m src.migrations
```

### 4. Проверка

```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Health check
curl http://83.147.246.172:8007/health
curl http://83.147.246.172:3007

# Автоматическая проверка (если скопирован deploy-check.sh)
bash deploy-check.sh 83.147.246.172
```

### 5. Полезные команды

```bash
# Логи
docker-compose -f docker-compose.prod.yml logs -f

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Остановка
docker-compose -f docker-compose.prod.yml down

# Обновление образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

---

📖 **Полная инструкция:** [`docs/guides/manual-deploy.md`](../../docs/guides/manual-deploy.md)

🚀 **Готово!**
- Frontend: http://83.147.246.172:3007
- API: http://83.147.246.172:8007/docs


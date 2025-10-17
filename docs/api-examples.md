# 📡 API Examples: systech-aidd Statistics API

> **Базовый URL:** http://localhost:8000  
> **Версия:** 0.1.0  
> **Статус:** Mock реализация (Sprint F01)

---

## 🚀 Быстрый старт

### Запуск API сервера

```bash
# Установка зависимостей
make install

# Запуск в dev режиме (с auto-reload)
make api-dev

# Или напрямую
uv run python -m src.api_main
```

Сервер запустится на `http://localhost:8000`

---

## 📋 Endpoints

### 1. Root - Информация о API

**Запрос:**
```bash
curl http://localhost:8000/
```

**Ответ:**
```json
{
  "status": "ok",
  "message": "Systech AIDD Statistics API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

---

### 2. Health Check

**Запрос:**
```bash
curl http://localhost:8000/health
```

**Ответ:**
```json
{
  "status": "healthy"
}
```

---

### 3. Dashboard Statistics - Основной endpoint

**Запрос:**
```bash
curl http://localhost:8000/api/stats/dashboard
```

**PowerShell (с форматированием):**
```powershell
(curl http://localhost:8000/api/stats/dashboard).Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Bash/Linux (с форматированием):**
```bash
curl http://localhost:8000/api/stats/dashboard | python -m json.tool
# или с jq
curl http://localhost:8000/api/stats/dashboard | jq
```

**Пример ответа:**
```json
{
  "overview": {
    "total_users": 369,
    "active_users_7d": 73,
    "active_users_30d": 213,
    "total_messages": 7495,
    "messages_7d": 1422,
    "messages_30d": 4192
  },
  "users": {
    "premium_count": 59,
    "premium_percentage": 15.99,
    "regular_count": 310,
    "by_language": {
      "ru": 231,
      "en": 104,
      "uk": 17,
      "other": 17
    }
  },
  "messages": {
    "avg_length": 93.0,
    "first_message_date": "2025-05-20T12:27:05.304128",
    "last_message_date": "2025-10-17T11:27:05.304128",
    "user_to_assistant_ratio": 1.03
  },
  "metadata": {
    "generated_at": "2025-10-17T12:27:05.304128",
    "is_mock": true
  }
}
```

---

## 🔧 Использование с различными инструментами

### curl (встроенный в Windows 10+)

```bash
# Базовый запрос
curl http://localhost:8000/api/stats/dashboard

# Только HTTP статус
curl -I http://localhost:8000/api/stats/dashboard

# С заголовками
curl -v http://localhost:8000/api/stats/dashboard

# Сохранить в файл
curl http://localhost:8000/api/stats/dashboard -o stats.json
```

### PowerShell

```powershell
# Invoke-RestMethod (парсит JSON автоматически)
$stats = Invoke-RestMethod -Uri "http://localhost:8000/api/stats/dashboard"
$stats.overview
$stats.users

# Invoke-WebRequest (raw response)
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/stats/dashboard"
$response.Content | ConvertFrom-Json
```

### httpie (установка: `pip install httpie`)

```bash
# Красивый вывод с цветами
http GET localhost:8000/api/stats/dashboard

# Только тело ответа
http --body GET localhost:8000/api/stats/dashboard

# Сохранить в файл
http GET localhost:8000/api/stats/dashboard > stats.json
```

### Python requests

```python
import requests
import json

# Получение статистики
response = requests.get("http://localhost:8000/api/stats/dashboard")
stats = response.json()

print(f"Total users: {stats['overview']['total_users']}")
print(f"Premium percentage: {stats['users']['premium_percentage']}%")

# Красивый вывод
print(json.dumps(stats, indent=2))
```

### JavaScript (fetch API)

```javascript
// В браузере или Node.js (с node-fetch)
fetch('http://localhost:8000/api/stats/dashboard')
  .then(response => response.json())
  .then(stats => {
    console.log('Total users:', stats.overview.total_users);
    console.log('Premium %:', stats.users.premium_percentage);
  });

// Async/await
const getStats = async () => {
  const response = await fetch('http://localhost:8000/api/stats/dashboard');
  const stats = await response.json();
  return stats;
};
```

---

## 📚 OpenAPI / Swagger Documentation

### Интерактивная документация

**Swagger UI** (рекомендуется для тестирования):
```
http://localhost:8000/docs
```

**ReDoc** (альтернативный вид):
```
http://localhost:8000/redoc
```

**OpenAPI JSON схема**:
```
http://localhost:8000/openapi.json
```

### Открыть Swagger UI

```bash
# Автоматически открыть в браузере
make api-docs

# Или вручную
# Windows
start http://localhost:8000/docs

# macOS
open http://localhost:8000/docs

# Linux
xdg-open http://localhost:8000/docs
```

---

## 🧪 Тестирование

### Быстрый тест работоспособности

```bash
# Через Makefile
make api-test

# Вручную
curl http://localhost:8000/health && echo "✅ API is healthy"
```

### Проверка валидации данных

Mock данные соблюдают следующие правила:
- `active_users_7d ≤ active_users_30d ≤ total_users`
- `messages_7d ≤ messages_30d ≤ total_messages`
- `premium_count + regular_count = total_users`
- `sum(by_language) = total_users`
- `metadata.is_mock = true`

### Нагрузочное тестирование (опционально)

```bash
# С помощью Apache Bench (если установлен)
ab -n 1000 -c 10 http://localhost:8000/api/stats/dashboard

# С помощью wrk (если установлен)
wrk -t2 -c10 -d30s http://localhost:8000/api/stats/dashboard
```

---

## 🔍 Troubleshooting

### API не отвечает

1. Проверьте, что сервер запущен:
```bash
make api-dev
```

2. Проверьте порт:
```powershell
netstat -ano | findstr :8000
```

3. Проверьте логи сервера в консоли запуска

### Ошибка импорта модулей

Убедитесь, что зависимости установлены:
```bash
make install
# или
uv sync
```

### Проблемы с CORS

Mock API настроен с `allow_origins=["*"]` для разработки.  
В production необходимо ограничить конкретными доменами frontend.

---

## 📝 Примечания

### Mock vs Real API

Текущая реализация использует **Mock данные** (Sprint F01):
- ✅ Готово для разработки frontend
- ✅ Не требует реальной БД
- ✅ Данные генерируются случайно при каждом запросе
- ⚠️ Данные не персистентны (не сохраняются)

В Sprint F05 будет реализован Real API с интеграцией PostgreSQL.

### Порт и конфигурация

По умолчанию API запускается на порту **8000**.  
Для изменения используйте переменные окружения:

```bash
# .env или export
API_HOST=0.0.0.0      # По умолчанию 0.0.0.0
API_PORT=8000         # По умолчанию 8000
API_RELOAD=true       # По умолчанию true (auto-reload в dev)
```

### CORS для frontend

API настроен с поддержкой CORS для работы с frontend.  
Frontend может быть запущен на любом порту (например, 3000, 5173).

---

## 📖 Связанные документы

- [Tasklist F01](tasklists/tasklist-F01.md) - Детальная информация о Sprint F01
- [Frontend Roadmap](frontend-roadmap.md) - План разработки frontend
- [План Sprint F01](../.cursor/plans/sprint-f01-mock-api-cacd9ae9.plan.md) - Детальный план реализации

---

**Дата создания:** 2025-10-17  
**Версия:** 1.0  
**Статус:** ✅ Готов к использованию


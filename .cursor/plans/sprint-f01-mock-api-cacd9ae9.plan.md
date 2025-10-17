<!-- cacd9ae9-b5d0-4dba-9181-fae855c54612 0559933b-403a-463c-9406-81e280d64637 -->
# Sprint F01: Mock API для дашборда статистики

## Цель спринта

Создать работающий Mock API endpoint для дашборда статистики с генерацией тестовых данных, готовый для интеграции с frontend.

## Основные метрики (базовый набор)

Согласно выбранному варианту, реализуем следующие метрики:

- Общее количество пользователей и активных за 7/30 дней
- Общее количество сообщений и сообщений за 7/30 дней  
- Соотношение Premium/обычных пользователей
- Средняя длина сообщения
- Даты первого и последнего сообщения

## Технические детали

### Framework и порт

- **Framework:** FastAPI (автогенерация OpenAPI, встроенная Pydantic валидация, async/await)
- **Порт:** 8000 (стандартный для FastAPI/uvicorn)
- **Host:** 0.0.0.0 (доступ со всех интерфейсов)

### Формат тестовых данных (Mock)

**Реалистичные диапазоны:**

- `total_users`: 100-500
- `active_users_7d`: 20-40% от total_users
- `active_users_30d`: 50-70% от total_users  
- `total_messages`: total_users × 10-30
- `messages_7d`: 15-25% от total_messages
- `messages_30d`: 40-60% от total_messages
- `premium_percentage`: 10-20%
- `avg_length`: 80-200 символов

**Логические связи:**

- `active_users_7d ≤ active_users_30d ≤ total_users`
- `messages_7d ≤ messages_30d ≤ total_messages`
- `premium_count + regular_count = total_users`
- Сумма `by_language` = `total_users`

**Временные метки:**

- `first_message_date`: 3-6 месяцев назад от текущей даты
- `last_message_date`: текущая дата минус 0-2 часа
- `generated_at`: точное текущее время

## Структура данных API Response

```json
{
  "overview": {
    "total_users": 287,
    "active_users_7d": 89,
    "active_users_30d": 178,
    "total_messages": 5843,
    "messages_7d": 1247,
    "messages_30d": 3156
  },
  "users": {
    "premium_count": 43,
    "premium_percentage": 14.98,
    "regular_count": 244,
    "by_language": {
      "ru": 186,
      "en": 78,
      "uk": 15,
      "other": 8
    }
  },
  "messages": {
    "avg_length": 127.8,
    "first_message_date": "2024-04-15T10:30:45Z",
    "last_message_date": "2024-10-17T16:45:12Z",
    "user_to_assistant_ratio": 1.02
  },
  "metadata": {
    "generated_at": "2024-10-17T16:47:30Z",
    "is_mock": true
  }
}
```

## Шаги реализации

### 1. Проектирование интерфейса StatCollector

**Файл:** `src/stats/collector.py` (новый)

Создать абстрактный базовый класс `StatCollector` с методом:

- `async def get_dashboard_stats() -> DashboardStats`

Это позволит легко переключаться между Mock и Real реализациями в будущем (Sprint F05).

### 2. Определение Pydantic моделей

**Файл:** `src/stats/models.py` (новый)

Создать Pydantic модели для строгой типизации:

- `OverviewStats` - общая статистика
- `UserStats` - статистика пользователей
- `MessageStats` - статистика сообщений  
- `DashboardStats` - корневая модель с вложенными stats

### 3. Реализация MockStatCollector

**Файл:** `src/stats/mock_collector.py` (новый)

Реализовать класс `MockStatCollector(StatCollector)`:

- Генерация реалистичных тестовых данных
- Использовать `random` для вариативности данных между запросами
- Соблюдать логические связи между метриками (active_users_7d < total_users и т.д.)

### 4. Создание FastAPI приложения

**Файл:** `src/api/app.py` (новый)

Создать FastAPI приложение с:

- GET endpoint `/api/stats/dashboard` - возвращает `DashboardStats`
- Автоматическая генерация OpenAPI документации
- CORS middleware для интеграции с frontend
- Dependency injection для `StatCollector`

### 5. Entrypoint для API сервера

**Файл:** `src/api_main.py` (новый)

Создать точку входа для запуска API:

- Инициализация `MockStatCollector`
- Конфигурация через переменные окружения (host, port)
- Запуск uvicorn сервера

### 6. Обновление зависимостей

**Файл:** `pyproject.toml`

Добавить новые зависимости:

- `fastapi` - веб-фреймворк для API
- `uvicorn[standard]` - ASGI сервер
- `pydantic` - валидация данных (возможно уже есть)

### 7. Команды в Makefile

**Файл:** `Makefile`

Добавить команды:

- `make api-dev` - запуск API сервера в dev режиме
- `make api-test` - проверка работоспособности через curl/httpie
- `make api-docs` - открыть Swagger UI в браузере

### 8. Документация

**Файл:** `docs/tasklists/tasklist-F01.md` (новый)

Создать tasklist для отслеживания прогресса спринта.

**Обновить:** `README.md`

- Добавить секцию про API
- Команды запуска и использования

## Ключевые файлы

```
src/
├── stats/
│   ├── __init__.py
│   ├── collector.py          # Абстрактный StatCollector
│   ├── models.py             # Pydantic модели
│   └── mock_collector.py     # Mock реализация
├── api/
│   ├── __init__.py
│   └── app.py               # FastAPI приложение
└── api_main.py              # Entrypoint для API
```

## Пример использования API

```bash
# Запуск сервера
make api-dev

# Получение статистики
curl http://localhost:8000/api/stats/dashboard

# Swagger UI
open http://localhost:8000/docs
```

## Критерии завершения

- ✅ API endpoint возвращает корректные Mock данные
- ✅ Swagger документация доступна и актуальна
- ✅ Команды Makefile работают
- ✅ Pydantic модели валидируют данные
- ✅ Mock данные реалистичны и соблюдают логические связи
- ✅ README обновлен с примерами использования
- ✅ Код проходит ruff и mypy проверки

## Принципы

- **KISS** - один endpoint, простая структура данных
- **API First** - контракт определен до реализации frontend
- **Mock First** - frontend разработка не зависит от реальной БД
- **Type Safety** - Pydantic для валидации, Mypy для статической проверки

## To-dos

### Реализация

- [ ] Добавить fastapi и uvicorn в pyproject.toml
- [ ] Спроектировать интерфейс StatCollector и Pydantic модели (src/stats/collector.py, src/stats/models.py)
- [ ] Реализовать MockStatCollector с генерацией тестовых данных (src/stats/mock_collector.py)
- [ ] Создать FastAPI приложение с endpoint /api/stats/dashboard (src/api/app.py)
- [ ] Создать entrypoint src/api_main.py для запуска API сервера
- [ ] Добавить команды в Makefile для работы с API (api-dev, api-test, api-docs)

### Тестирование

- [ ] Создать примеры запросов к API для тестирования (curl/httpie команды)
- [ ] Протестировать API endpoint и проверить валидацию Pydantic моделей
- [ ] Проверить Swagger UI документацию и актуальность OpenAPI схемы

### Документация и финализация

- [ ] Создать tasklist-F01.md для отслеживания прогресса спринта
- [ ] Обновить README.md с секцией про API и примерами использования
- [ ] Добавить ссылку на этот план в таблицу спринтов в frontend-roadmap.md
- [ ] Актуализировать frontend-roadmap.md после выполнения спринта (статус F01 → "Завершен")
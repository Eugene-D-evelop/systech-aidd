<!-- baab1c33-fa96-4137-b147-3764a9616bec dc771b22-fbec-460c-b1ec-3c8f140b02e0 -->
# План Спринта D1 - Build & Publish

## Обзор

Автоматизировать сборку и публикацию трех Docker образов (bot, api, frontend) в GitHub Container Registry (ghcr.io) при изменениях в main ветке. Образы будут публично доступны для использования в будущих спринтах D2 (ручной deploy) и D3 (авто deploy).

## Контекст

- **Репозиторий:** `Eugene-D-evelop/systech-aidd`
- **Текущее состояние:** Dockerfile созданы в спринте D0, локальная сборка работает через `docker-compose up --build`
- **Registry:** `ghcr.io/eugene-d-evelop/systech-aidd-{service}`
- **Trigger:** Push в main ветку
- **Тестирование:** Отдельная ветка `feature/github-actions-setup`

## Этапы реализации

### 1. Документация GitHub Actions

**Файл:** `devops/doc/github-actions-guide.md`

Создать краткую инструкцию (на русском), включающую:

- Что такое GitHub Actions и workflow
- Принципы работы с triggers (on: push, pull_request)
- Работа с Pull Request и проверка CI
- Matrix strategy для сборки нескольких образов
- GitHub Container Registry (ghcr.io) - публикация и настройка публичного доступа
- Работа с GitHub Secrets и GITHUB_TOKEN (автоматический токен с правами на ghcr.io)

### 2. Создание GitHub Actions Workflow

**Файл:** `.github/workflows/build.yml`

Workflow должен включать:

```yaml
name: Build and Publish Docker Images

on:
  push:
    branches: [ main ]

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [bot, api, frontend]
    steps:
      - Checkout кода
      - Login в ghcr.io с GITHUB_TOKEN
      - Setup Docker Buildx для кэширования
      - Определение контекста и Dockerfile для каждого сервиса
      - Build образа с кэшированием слоев
      - Tag образа: latest и commit SHA
      - Push в ghcr.io
```

**Ключевые особенности:**

- Matrix strategy для параллельной сборки 3 сервисов
- Кэширование Docker layers через buildx и GitHub Cache
- Динамическое определение context и dockerfile для bot/api (корень) и frontend (./frontend)
- Тегирование: `latest` и `sha-${GITHUB_SHA:0:7}`

**Детальная спецификация Matrix Strategy:**

```yaml
strategy:
  matrix:
    include:
      - service: bot
        context: .
        dockerfile: ./Dockerfile
        image: ghcr.io/eugene-d-evelop/systech-aidd-bot
      - service: api
        context: .
        dockerfile: ./Dockerfile
        image: ghcr.io/eugene-d-evelop/systech-aidd-api
      - service: frontend
        context: ./frontend
        dockerfile: ./frontend/Dockerfile
        image: ghcr.io/eugene-d-evelop/systech-aidd-frontend
```

**Build Args (MVP решение):**

Для MVP build args НЕ используются:

- Bot/API: все переменные через environment в docker-compose
- Frontend: dev режим (pnpm dev), NEXT_PUBLIC_API_URL через environment в runtime

### 3. Версии docker-compose.yml

**Создать структуру файлов:**

```
docker-compose.yml              # Локальная разработка (build из исходников)
docker-compose.prod.yml         # Production (образы из ghcr.io)
```

**docker-compose.yml** - без изменений, для локальной разработки с hot-reload

**docker-compose.prod.yml** - использует готовые образы:

```yaml
services:
  bot:
    image: ghcr.io/eugene-d-evelop/systech-aidd-bot:latest
    # без build секции, без volume mounts для src
  api:
    image: ghcr.io/eugene-d-evelop/systech-aidd-api:latest
  frontend:
    image: ghcr.io/eugene-d-evelop/systech-aidd-frontend:latest
```

**Переключение режимов:**

- Разработка: `docker-compose up`
- Production: `docker-compose -f docker-compose.prod.yml up`

### 4. Настройка публичного доступа к образам

После первой публикации образов в ghcr.io необходимо сделать их публичными:

1. Перейти на страницу пакета: `https://github.com/users/Eugene-D-evelop/packages/container/systech-aidd-{service}/settings`
2. В разделе "Danger Zone" → "Change package visibility" → выбрать "Public"
3. Повторить для всех трех образов (bot, api, frontend)

Это позволит скачивать образы без авторизации: `docker pull ghcr.io/eugene-d-evelop/systech-aidd-bot:latest`

### 5. Обновление документации

**README.md** - добавить секцию "🚀 CI/CD":

```markdown
## 🚀 CI/CD

[![Build Status](https://github.com/Eugene-D-evelop/systech-aidd/actions/workflows/build.yml/badge.svg)](https://github.com/Eugene-D-evelop/systech-aidd/actions/workflows/build.yml)

### Docker образы

Проект автоматически собирается и публикуется в GitHub Container Registry:

- Bot: `ghcr.io/eugene-d-evelop/systech-aidd-bot:latest`
- API: `ghcr.io/eugene-d-evelop/systech-aidd-api:latest`
- Frontend: `ghcr.io/eugene-d-evelop/systech-aidd-frontend:latest`

### Запуск из готовых образов

# Скачать последние образы и запустить
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

### Локальная разработка

# Сборка из исходников с hot-reload
docker-compose up --build
```

**devops/doc/devops-roadmap.md** - обновить статус D1:

- Изменить статус на "✅ Done"
- Добавить ссылку на план в колонке "План"

**Создать:** `devops/doc/plans/d1-build-publish-plan.md` - этот план

### 6. Процесс тестирования

**Этап 1: Тестовая ветка**

1. Создать ветку `feature/github-actions-setup`
2. Добавить workflow файл `.github/workflows/build.yml` с trigger на эту ветку
3. Сделать push и проверить запуск workflow
4. Убедиться, что все 3 образа собираются успешно

**Этап 2: Публикация в main**

1. Изменить trigger на `push: branches: [main]`
2. Сделать merge в main через PR
3. Проверить автоматический запуск workflow
4. Убедиться, что образы опубликованы в ghcr.io

**Этап 3: Настройка публичного доступа**

1. Сделать все 3 пакета публичными через настройки GitHub
2. Проверить скачивание без авторизации

**Этап 4: Тестирование prod режима**

```bash
# Скачать образы из registry
docker-compose -f docker-compose.prod.yml pull

# Запустить
docker-compose -f docker-compose.prod.yml up -d

# Проверить работу всех сервисов
curl http://localhost:8000/health
curl http://localhost:3000

# Остановить
docker-compose -f docker-compose.prod.yml down
```

**Примечание о CI на Pull Request:**

Для MVP автоматическая проверка Pull Request сознательно исключена:

- ✅ Тестирование workflow на feature-ветке (Этап 1 - вручную)
- ✅ Автоматическая сборка при merge в main (Этап 2)
- ❌ Автоматическая сборка на каждый PR (добавим в будущих итерациях)

Это экономит GitHub Actions минуты и ускоряет MVP реализацию.

### 7. Итоговая документация

**Создать:** `devops/doc/reports/d1-summary.md`

Включить:

- Ссылки на опубликованные образы
- Команды для работы с образами
- Скриншоты успешных workflow runs
- Подтверждение публичного доступа
- Готовность к спринтам D2 и D3

## Что НЕ делаем (MVP подход)

- ❌ Lint checks в CI (добавим позже)
- ❌ Тесты в CI (добавим позже)
- ❌ Security scanning (Trivy, Snyk)
- ❌ Multi-platform builds (linux/amd64, linux/arm64)
- ❌ Сборка на Pull Request (только на push в main)
- ❌ Автоматическое создание releases
- ❌ Semantic versioning (пока только latest + sha)

## Критерии успеха

- ✅ Workflow запускается при push в main
- ✅ Все 3 образа собираются параллельно через matrix
- ✅ Образы публикуются в ghcr.io с тегами latest и sha
- ✅ Образы доступны публично без авторизации
- ✅ `docker-compose.prod.yml` успешно скачивает и запускает образы из registry
- ✅ README содержит badge статуса сборки
- ✅ Документация обновлена и содержит инструкции по использованию

## Файлы для создания/изменения

**Новые файлы:**

- `.github/workflows/build.yml` - GitHub Actions workflow
- `docker-compose.prod.yml` - конфигурация для production образов
- `devops/doc/github-actions-guide.md` - руководство по GitHub Actions
- `devops/doc/plans/d1-build-publish-plan.md` - этот план
- `devops/doc/reports/d1-summary.md` - итоговый отчет

**Обновить:**

- `README.md` - добавить секцию CI/CD и badge
- `devops/doc/devops-roadmap.md` - обновить статус D1

### To-dos

- [ ] Создать devops/doc/github-actions-guide.md с руководством по GitHub Actions, triggers, matrix strategy, и ghcr.io
- [ ] Создать .github/workflows/build.yml с matrix strategy для сборки 3 образов (bot, api, frontend)
- [ ] Создать docker-compose.prod.yml для использования образов из ghcr.io вместо локальной сборки
- [ ] Обновить README.md: добавить секцию CI/CD с badge и инструкциями по работе с образами из registry
- [ ] Создать devops/doc/plans/d1-build-publish-plan.md с детальным планом спринта
- [ ] Обновить devops/doc/devops-roadmap.md: добавить ссылку на план D1 и обновить статус после завершения
- [ ] Создать devops/doc/reports/d1-summary.md с инструкциями по тестированию и итоговым отчетом
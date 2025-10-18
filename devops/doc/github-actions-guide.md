# Руководство по GitHub Actions

## Введение

GitHub Actions — это встроенная CI/CD платформа GitHub для автоматизации процессов разработки, тестирования и развертывания прямо из вашего репозитория.

### Основные понятия

**Workflow (рабочий процесс)** — автоматизированный процесс, который состоит из одного или нескольких jobs. Определяется в YAML файле в директории `.github/workflows/`.

**Job (задача)** — набор шагов (steps), которые выполняются на одном runner'е. Jobs могут выполняться последовательно или параллельно.

**Step (шаг)** — отдельная команда или action, которую нужно выполнить.

**Runner** — сервер, на котором выполняется workflow. GitHub предоставляет бесплатные runner'ы: `ubuntu-latest`, `windows-latest`, `macos-latest`.

**Action** — готовое приложение, которое выполняет часто повторяющуюся задачу (например, `actions/checkout` для клонирования кода).

## Triggers (триггеры запуска)

Workflow может запускаться на различные события:

### Push в ветку

```yaml
on:
  push:
    branches: [ main, develop ]
```

Запускается при каждом push в указанные ветки.

### Pull Request

```yaml
on:
  pull_request:
    branches: [ main ]
```

Запускается при создании/обновлении PR в указанные ветки. Полезно для проверки кода перед merge.

### Комбинация событий

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### Ручной запуск

```yaml
on:
  workflow_dispatch:
```

Позволяет запустить workflow вручную через UI GitHub.

### Schedule (расписание)

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Каждый день в 2:00 UTC
```

## Работа с Pull Request

### Проверка кода в PR

При настройке trigger на `pull_request`, GitHub Actions автоматически:

1. Запускает workflow при создании PR
2. Обновляет статус проверки при push новых коммитов
3. Показывает результаты в интерфейсе PR
4. Блокирует merge, если проверки не прошли (опционально)

### Настройка защиты веток

В настройках репозитория (`Settings` → `Branches` → `Branch protection rules`) можно:

- Требовать прохождения статус проверок перед merge
- Требовать актуальности ветки перед merge
- Требовать review от других разработчиков

### Типичный workflow для PR

```yaml
name: PR Checks

on:
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: make lint
  
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test
```

## Matrix Strategy

Matrix strategy позволяет запустить job несколько раз с разными параметрами **параллельно**.

### Базовый пример

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: [3.9, 3.10, 3.11]
    steps:
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.version }}
```

Этот job запустится 3 раза параллельно для Python 3.9, 3.10 и 3.11.

### Matrix с несколькими переменными

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
```

Создаст 4 комбинации: ubuntu+18, ubuntu+20, windows+18, windows+20.

### Include для кастомных комбинаций

```yaml
strategy:
  matrix:
    include:
      - service: bot
        context: .
        dockerfile: ./Dockerfile
      - service: api
        context: .
        dockerfile: ./Dockerfile
      - service: frontend
        context: ./frontend
        dockerfile: ./frontend/Dockerfile
```

Каждый элемент `include` создает отдельный запуск job с указанными параметрами. Доступ к значениям: `${{ matrix.service }}`, `${{ matrix.context }}`.

### Параллельность и fail-fast

```yaml
strategy:
  matrix:
    service: [bot, api, frontend]
  fail-fast: false  # Продолжать даже если один job упал
  max-parallel: 3   # Максимум параллельных запусков
```

## GitHub Container Registry (ghcr.io)

GitHub Container Registry — это реестр Docker образов, интегрированный с GitHub.

### Преимущества ghcr.io

- ✅ Бесплатный для публичных репозиториев
- ✅ Интеграция с GitHub Packages
- ✅ Тот же аккаунт, что и для кода
- ✅ Поддержка публичных и приватных образов
- ✅ Хорошая интеграция с GitHub Actions

### Адресация образов

Формат: `ghcr.io/OWNER/IMAGE_NAME:TAG`

Примеры:
```
ghcr.io/eugene-d-evelop/systech-aidd-bot:latest
ghcr.io/eugene-d-evelop/systech-aidd-api:v1.2.3
ghcr.io/eugene-d-evelop/systech-aidd-frontend:sha-abc1234
```

### Публикация образа

```yaml
steps:
  # Логин в ghcr.io
  - name: Login to GitHub Container Registry
    uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
  
  # Build и push
  - name: Build and push
    uses: docker/build-push-action@v5
    with:
      context: .
      push: true
      tags: ghcr.io/${{ github.repository_owner }}/my-image:latest
```

### Настройка публичного доступа

По умолчанию образы **приватные**. Чтобы сделать их публичными:

1. Перейти на страницу пакета: `https://github.com/users/USERNAME/packages/container/PACKAGE_NAME/settings`
2. Прокрутить до секции **"Danger Zone"**
3. Нажать **"Change package visibility"**
4. Выбрать **"Public"** и подтвердить

После этого образы можно скачивать без авторизации:
```bash
docker pull ghcr.io/eugene-d-evelop/systech-aidd-bot:latest
```

### Связывание пакета с репозиторием

В настройках пакета можно связать его с репозиторием для удобства навигации.

## Secrets и GITHUB_TOKEN

### GitHub Secrets

GitHub Secrets — безопасное хранилище для чувствительных данных (API ключи, токены, пароли).

**Добавление секрета:**
1. `Settings` → `Secrets and variables` → `Actions`
2. `New repository secret`
3. Указать имя и значение

**Использование:**
```yaml
steps:
  - name: Use secret
    env:
      API_KEY: ${{ secrets.MY_API_KEY }}
    run: echo "API key is set"
```

⚠️ **Важно:** Секреты никогда не выводятся в логи (маскируются автоматически).

### GITHUB_TOKEN

`GITHUB_TOKEN` — автоматический токен, который GitHub создает для каждого workflow run.

**Возможности:**
- Чтение кода репозитория
- Публикация в GitHub Packages (ghcr.io)
- Создание комментариев в Issues/PR
- Обновление статусов проверок

**Использование:**
```yaml
steps:
  - name: Use GITHUB_TOKEN
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: gh api /repos/${{ github.repository }}
```

**Для ghcr.io:**
```yaml
- name: Login to ghcr.io
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Permissions для GITHUB_TOKEN

По умолчанию `GITHUB_TOKEN` имеет ограниченные права. Для ghcr.io нужны права на запись пакетов:

```yaml
permissions:
  contents: read      # Чтение кода
  packages: write     # Публикация образов в ghcr.io
```

## Кэширование в GitHub Actions

### GitHub Cache для Docker layers

Docker Buildx поддерживает кэширование слоев через GitHub Cache:

```yaml
- name: Setup Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/user/image:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Преимущества:**
- Ускоряет повторные сборки
- Использует GitHub Cache (10 GB на репозиторий)
- Автоматически управляется

### Cache для зависимостей

```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

## Типичные паттерны

### Build и publish Docker образа

```yaml
name: Build and Publish

on:
  push:
    branches: [ main ]

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/my-app:latest
            ghcr.io/${{ github.repository_owner }}/my-app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Matrix для нескольких сервисов

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: bot
            context: .
            dockerfile: ./Dockerfile
          - service: frontend
            context: ./frontend
            dockerfile: ./frontend/Dockerfile
    steps:
      - uses: actions/checkout@v4
      
      - name: Build ${{ matrix.service }}
        run: docker build -f ${{ matrix.dockerfile }} ${{ matrix.context }}
```

## Отладка workflows

### Просмотр логов

Логи доступны в интерфейсе GitHub:
- `Actions` → выбрать workflow run → выбрать job → раскрыть step

### Debug logging

Включить подробные логи:
1. `Settings` → `Secrets and variables` → `Actions`
2. Добавить секрет `ACTIONS_STEP_DEBUG` со значением `true`

### Локальная отладка

Использовать [act](https://github.com/nektos/act) для запуска workflows локально:

```bash
# Установка
brew install act  # macOS
# или скачать с GitHub

# Запуск workflow
act push

# Запуск конкретного job
act -j build
```

## Best Practices

1. **Минимальные permissions:** Указывайте только необходимые права для `GITHUB_TOKEN`
2. **Кэширование:** Используйте кэш для ускорения сборки
3. **Fail-fast: false** для matrix, если хотите видеть все результаты
4. **Тегирование образов:** Используйте несколько тегов (latest, sha, версия)
5. **Secrets:** Никогда не храните чувствительные данные в коде
6. **Условное выполнение:** Используйте `if:` для условных шагов
7. **Timeout:** Устанавливайте таймауты для long-running jobs

## Полезные ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry Guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)


# 🚀 Быстрый старт

## Первый запуск

```bash
# 1. Установить зависимости
make install

# 2. Создать .env файл
cp .env.example .env  # и заполнить токены

# 3. Запустить бота
make run
```

## Запуск через UI

### 🤖 Запустить бота

1. **Быстрый способ:** `Ctrl+Shift+R`
2. **Или:** `Ctrl+Shift+D` → выбрать "🤖 Bot: Run (Normal)" → `F5`
3. **Или:** `Ctrl+Shift+P` → "Tasks: Run Task" → "🤖 Start Bot"

### 🐛 Отладка бота

1. Поставить breakpoint: `F9` в нужной строке
2. `Ctrl+Shift+D` → "🤖 Bot: Run (Debug Mode)" → `F5`
3. Отправить сообщение боту → выполнение остановится на breakpoint

### 🧪 Тесты

- **Все тесты:** `Ctrl+Shift+P` → "Test: Run All Tests"
- **Юнит-тесты:** `Ctrl+Shift+T`
- **Один тест:** открыть Testing панель → нажать ▶️ рядом с тестом

## Основные команды

| Что нужно | Команда | Горячие клавиши |
|-----------|---------|-----------------|
| Запустить бота | `make run` | `Ctrl+Shift+R` |
| Все тесты + coverage | `make test` | - |
| Юнит-тесты | `make test-unit` | `Ctrl+Shift+T` |
| Проверка кода | `make lint` | - |
| Форматирование | `make format` | `Ctrl+Shift+F` |
| CI проверка | `make ci` | `Ctrl+Shift+C` |

## Горячие клавиши

### Отладка
- `F5` - Запустить/Продолжить
- `Shift+F5` - Остановить
- `F9` - Breakpoint
- `F10` - Следующая строка
- `F11` - Войти в функцию

### Навигация
- `Ctrl+P` - Найти файл
- `F12` - Перейти к определению
- `Ctrl+Shift+O` - Символы в файле

### Тестирование
- `Ctrl+Shift+T` - Запустить юнит-тесты
- Testing панель - иконка колбы 🧪 слева

## Структура проекта

```
src/
├── main.py          # Точка входа ← начни отсюда
├── bot.py           # Telegram bot
├── handlers.py      # Обработчики сообщений
├── llm_client.py    # OpenRouter API
├── conversation.py  # История диалогов
└── config.py        # Конфигурация

tests/
├── test_*.py        # Юнит-тесты
└── test_llm_client.py  # Интеграционные (требуют .env)
```

## Workflow

1. **Перед началом работы:**
   ```bash
   make ci  # Проверить что все ОК
   ```

2. **Разработка:**
   - Писать код
   - Сохранить → авто-форматирование
   - Тесты обновляются автоматически

3. **Перед коммитом:**
   ```bash
   make ci  # lint + test-unit
   ```

4. **Коммит:**
   ```bash
   git add .
   git commit -m "feat: описание изменений"
   git push
   ```

## Полезные ссылки

- 📖 Полная документация: `.vscode/README.md`
- 📋 План проекта: `docs/tasklist.md`
- 🎯 Техническое видение: `docs/vision.md`
- 📝 Соглашения: `.cursor/rules/conventions.mdc`

## Troubleshooting

### "Python интерпретатор не найден"
`Ctrl+Shift+P` → "Python: Select Interpreter" → выбрать `.venv\Scripts\python.exe`

### "Тесты не обнаруживаются"
`Ctrl+Shift+P` → "Test: Refresh Tests"

### "Бот не запускается"
Проверить `.env` файл - должны быть заполнены `TELEGRAM_BOT_TOKEN` и `OPENROUTER_API_KEY`

---

**Нужна помощь?** Смотри `.vscode/README.md` для детальной документации


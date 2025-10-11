# VS Code / Cursor Configuration

## 🤖 Запуск бота через UI

### Способ 1: Run & Debug (Рекомендуется)

1. Откройте панель **Run & Debug** (`Ctrl+Shift+D`)
2. Выберите одну из конфигураций:
   - **🤖 Bot: Run (Normal)** - обычный запуск с логами INFO
   - **🤖 Bot: Run (Debug Mode)** - запуск с DEBUG логами и breakpoints
   - **🤖 Bot: Run via Make** - запуск через `make run`
3. Нажмите **F5** или кнопку ▶️

**Остановка бота:**
- `Ctrl+C` в терминале
- Кнопка 🛑 Stop в панели Debug
- `Shift+F5` (горячая клавиша)

### Способ 2: Tasks

1. Откройте Command Palette (`Ctrl+Shift+P`)
2. Введите "Tasks: Run Task"
3. Выберите **🤖 Start Bot**

**Доступные задачи:**
- `🤖 Start Bot` - быстрый запуск бота
- `🧪 Run All Tests` - все тесты с coverage
- `🧪 Run Unit Tests` - только юнит-тесты
- `🔍 Lint Code` - проверка ruff + mypy
- `✨ Format Code` - форматирование кода
- `🚀 CI Check` - полная проверка перед коммитом
- `📦 Install Dependencies` - установка зависимостей
- `🧹 Clean Cache` - очистка Python кеша

### Способ 3: Кнопка запуска

1. Откройте `src/main.py`
2. Нажмите **Run Python File** в правом верхнем углу
3. Или используйте `Ctrl+F5`

### Отладка бота

Для отладки с breakpoints:
1. Поставьте breakpoint (F9) в нужном месте (например, в `handlers.py`)
2. Выберите **🤖 Bot: Run (Debug Mode)**
3. Нажмите F5
4. Отправьте сообщение боту в Telegram
5. Выполнение остановится на breakpoint

**Полезные горячие клавиши при отладке:**
- `F5` - Continue
- `F10` - Step Over (следующая строка)
- `F11` - Step Into (войти в функцию)
- `Shift+F11` - Step Out (выйти из функции)
- `Ctrl+Shift+F5` - Restart
- `Shift+F5` - Stop

## 🧪 Запуск тестов через UI

### Активация Test Explorer

1. Откройте панель Testing (иконка колбы в левой панели или `Ctrl+Shift+P` → "Test: Focus on Test Explorer View")
2. Тесты автоматически обнаружатся при открытии проекта
3. Используйте кнопки рядом с тестами для запуска/отладки

### Быстрые команды

- **Запустить все тесты**: кнопка ▶️ в Test Explorer
- **Запустить файл тестов**: кнопка ▶️ рядом с файлом
- **Запустить один тест**: кнопка ▶️ рядом с функцией
- **Отладить тест**: кнопка 🐞 (breakpoint будут работать)
- **Повторить последний запуск**: `Ctrl+Shift+P` → "Test: Rerun Last Run"

### Фильтрация тестов

По умолчанию запускаются только **юнит-тесты** (без маркера `integration`).

Для запуска интеграционных тестов:
1. Откройте `settings.json`
2. Измените `python.testing.pytestArgs`:
   ```json
   "python.testing.pytestArgs": [
       "tests",
       "-v",
       "--tb=short",
       "--strict-markers"
       // Убрать: "-m", "not integration"
   ]
   ```

### Coverage через UI

Для отображения coverage в редакторе установите расширение:
- **Coverage Gutters** (`ryanluker.vscode-coverage-gutters`)

После запуска `make test` или `make test-unit` coverage подсветится в файлах.

## 🐛 Отладка

### Доступные конфигурации

1. **Python: Debug Tests** - отладка всех юнит-тестов
2. **Python: Debug Current Test File** - отладка открытого файла
3. **Python: Debug Integration Tests** - отладка интеграционных тестов
4. **Python: Run Bot** - запуск бота с отладчиком

### Использование

1. Поставьте breakpoint (F9) в нужной строке
2. Откройте Run & Debug (Ctrl+Shift+D)
3. Выберите конфигурацию
4. Нажмите F5 для запуска

## ⚙️ Автоматизация

### Format on Save

Код автоматически форматируется при сохранении файла через `ruff`.

### Auto Test Discovery

Тесты автоматически обнаруживаются при сохранении файлов в папке `tests/`.

### Organize Imports

Импорты автоматически сортируются при сохранении.

## 📦 Рекомендуемые расширения

При открытии проекта VS Code/Cursor предложит установить:

- **Python** - базовая поддержка Python
- **Pylance** - быстрая типизация и IntelliSense
- **Ruff** - линтинг и форматирование
- **Error Lens** - подсветка ошибок прямо в редакторе
- **Even Better TOML** - подсветка `pyproject.toml`

## ⌨️ Горячие клавиши

### Быстрый доступ к командам

| Клавиши | Действие |
|---------|----------|
| `Ctrl+Shift+R` | 🤖 Запустить бота |
| `Ctrl+Shift+T` | 🧪 Запустить юнит-тесты |
| `Ctrl+Shift+F` | ✨ Форматировать код |
| `Ctrl+Shift+C` | 🚀 CI проверка |
| `Ctrl+Shift+E` | Показать результаты тестов |

### Стандартные клавиши VS Code

| Клавиши | Действие |
|---------|----------|
| `F5` | Запустить/продолжить отладку |
| `Ctrl+F5` | Запустить без отладки |
| `Shift+F5` | Остановить отладку |
| `Ctrl+Shift+F5` | Перезапустить отладку |
| `F9` | Поставить/убрать breakpoint |
| `F10` | Step Over (следующая строка) |
| `F11` | Step Into (войти в функцию) |
| `Shift+F11` | Step Out (выйти из функции) |
| `Ctrl+Shift+D` | Открыть панель Run & Debug |
| `Ctrl+Shift+P` | Command Palette |

### Быстрая навигация

- `Ctrl+P` - быстрый переход к файлу
- `Ctrl+Shift+O` - перейти к символу в файле
- `Ctrl+T` - найти символ в проекте
- `F12` - перейти к определению
- `Alt+F12` - посмотреть определение (peek)

## 🔧 Troubleshooting

### Тесты не обнаруживаются

1. Проверьте, что выбран правильный Python интерпретатор:
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Выберите `.venv\Scripts\python.exe`

2. Перезагрузите Test Discovery:
   - `Ctrl+Shift+P` → "Test: Refresh Tests"

3. Проверьте Output панель:
   - View → Output → Python Test Log

### Virtual Environment не активируется

Убедитесь, что виртуальное окружение создано:
```bash
make install
```

### Mypy не работает

Установите расширение Python и перезагрузите окно:
- `Ctrl+Shift+P` → "Developer: Reload Window"

---

**Дополнительно:** см. `Makefile` для команд терминала


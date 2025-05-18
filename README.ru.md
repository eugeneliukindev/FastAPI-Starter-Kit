# FastAPI Starter Kit 🚀

Легкий и готовый к использованию шаблон для разработки API на **FastAPI**. Начните работу за считанные минуты без сложной настройки!

## Зачем использовать этот шаблон?

Этот стартовый набор создан, чтобы ускорить разработку на FastAPI, избавляя от:

- 🛠️ **Настройки базы данных**
- ⚙️ **Конфигурации окружения**
- 📂 **Долгой инициализации проекта и его структуры**
- 🗂️ **Ручной настройки моделей SQLAlchemy и схем Pydantic**

### Особенности

- ✅ **Поддержка типизации** с [Mypy](https://mypy.readthedocs.io/en/stable/)
- 🧹 **Качество кода** с линтером и форматтером [Ruff](https://docs.astral.sh/ruff/)
- 📦 **Управление зависимостями** через [Poetry](https://python-poetry.org/)
- 🐳 **Docker-образ Postgres** для быстрой настройки базы данных
- 🔄 **Миграции Alembic** для удобного управления схемой базы данных

## Начало работы

Следуйте этим шагам, чтобы настроить и запустить проект локально.

### Требования

- 🐍 Python 3.12+
- 📦 [Poetry](https://python-poetry.org/docs/#installation) для управления зависимостями
- 🐳 [Docker](https://www.docker.com/get-started) (опционально, для настройки Postgres)

### Установка

1. **Клонирование репозитория**

   Через HTTPS:
   ```bash
   git clone https://github.com/eugeneliukindev/FastAPI-Starter-Kit.git
   ```

   Через SSH (рекомендуется):
   ```bash
   git clone git@github.com:eugeneliukindev/FastAPI-Starter-Kit.git
   ```

2. **Установка зависимостей**

   Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями. Подробности в файле [pyproject.toml](pyproject.toml).

   *Опционально*: Настройте Poetry для создания виртуального окружения в корне проекта:
   ```bash
   poetry config virtualenvs.in-project true
   ```

   Установите зависимости:

   С dev-зависимостями (для разработки):
   ```bash
   poetry install
   ```

   Без dev-зависимостей (для продакшена):
   ```bash
   poetry install --without dev
   ```

3. **Настройка базы данных**

   Используйте предоставленный Docker Compose файл для запуска Postgres:
   ```bash
   docker compose up -d
   ```

   *Примечание*: Убедитесь, что [Docker](https://www.docker.com/) установлен и запущен.

4. **Создание миграций Alembic**

   Сгенерируйте и примените миграции базы данных с помощью Alembic:
   ```bash
   alembic revision --autogenerate -m "create tables" && alembic upgrade head
   ```

5. **Запуск приложения**

   Перейдите в директорию приложения и запустите сервер FastAPI:
   ```bash
   cd fastapi-app && python main.py
   ```

   Ваше API теперь работает! Доступно по адресу `http://localhost:8000` (или настроенному порту).

## Использование

- 📚 **Документация API**: Автоматически генерируется FastAPI и доступна по `/docs` (Swagger UI) или `/redoc`
- 🛠️ **Инструменты для разработки**:
  - Выполните `mypy .` для проверки типов
  - Выполните `ruff check .` для linting
  - Выполните `ruff format .` для форматирования кода

   
## Вклад в проект

Мы приветствуем любые улучшения! Чтобы внести вклад:

1. Сделайте форк репозитория
2. Создайте ветку для новой функциональности (`git checkout -b feature/YourFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add YourFeature'`)
4. Отправьте ветку в репозиторий (`git push origin feature/YourFeature`)
5. Откройте Pull Request

## Лицензия

Проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE.txt).

---

Удачного кодинга! 🎉 Если у вас есть вопросы или нужна помощь, создайте issue в репозитории.

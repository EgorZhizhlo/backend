# Описание проекта
## Backend модуль
    Проект представляет собой RESTful API, разработанный с использованием фреймворка FastAPI, который работает под
    управлением ASGI сервера Uvicorn и развернут с помощью Docker Compose. В проекте реализованы три основных роутера:

    * Session – для управления сессиями пользователей.
    * LLMs – для взаимодействия с языковой моделью(Large Language Models).
    * Params – для обработки параметров запросов и конфигурационных данных.
    
    Для работы с базой данных используется SQLAlchemy AsyncIO и драйвер AsyncPG для асинхронных операций с PostgreSQL.
    Миграции базы данных управляются с помощью Alembic. Для чтения файлов различных форматов используются библиотеки 
    PyPDF2 и Docx, а также BeautifulSoup для парсинга HTML-документов. Для обращения к внешним сервисам применяется 
    библиотека AIOHTTP. Для балансировки нагрузки использовался Nginx.

## Установка и запуск проекта

### Преднастройка PostgreSQL
    git clone https://github.com/EgorZhizhlo/backend.git
    cd backend
    docker network create shared-network
    docker network create network
    cd pg
    nano .env

#### Настройка .env
    * CONTAINER_NAME="название контейнера"
    * POSTGRES_USER="имя пользователя"
    * POSTGRES_PASSWORD="пароль"
    * POSTGRES_DB="название БД"
    * POSTGRES_PORT="порт"

### Запуск PostgreSQL
    docker compose up --build -d

#### После деплоя база данных будет доступна к локальному подключению внутри VDS и др.

### Запуск API
    cd -
    docker compose up --build -d
#### Создание и отслеживание миграций
    docker compose exec <название контейнера API> alembic upgrade head
    docker compose exec <название контейнера API> alembic --autogenerate -m "Create database migrations"
    docker compose exec <название контейнера API> alembic upgrade head

##### После запуска проект будет располагаться по адрессу http://<твой ip или localhost>

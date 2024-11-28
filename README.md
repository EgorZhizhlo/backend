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
## Описание эндпоинтов
    * Сессия
        - POST /session/create
            Создает новую сессию и возвращает её идентификатор.
        - GET /session/get_uuid
            Получает UUID текущей сессии.
    * LLM
        - POST /llm/load_file
            Загружает локальный файл и индексирует его для дальнейшей обработки языком моделей (LLM).
        - POST /llm/load_url
            Загружает контент по URL и индексирует его для дальнейшей обработки языком моделей (LLM).
        - POST /llm/request
            Отправляет запрос к языку моделей (LLM) и получает ответ.
        - GET /llm/get_split
            Возвращает информацию о разбиении контента на части для обработки языком моделей (LLM).
    * Параметры
        - GET /params/get
            Получает текущие параметры конфигурации.
        - PUT /params/change
            Обновляет параметры конфигурации.

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

##### После запуска проект будет располагаться по адрессу http://<твой ip или localhost>:81

# backend

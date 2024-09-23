# TODO:
1. Exchange class for cross-converting (ie BTH/ETH)
2. Execution will block in main thread
3. Clear DB on shutdown
4. Sendmail
..

# Сборка приложения:
1. Клонировать репозиторий и перейти в корень приложения
2. Запустить сборку образа приложения:  
`docker build -t app_bitcoin_monitoring .`  
3. Запустить контейнеры БД и приложения (веб-сервер)  
`docker compose up`

# Инструкции по запуску:
1. Установить Python 3.12+
2. Перейти в каталог приложения и установить окружение  
`pip install -r requirements.txt`
3. Альтернативная установка через Pipenv (необязательно)  
`pip install pipenv`  
`pipenv install`
4. Запустить скрипт для мониторинга:
`pythom src\main.py`

# REST API:
Web-server по адресу http://localhost:5000

Получение всех записей
`GET localhost:5000`

Получение записи по ID
`GET localhost:5000/{id}`

Добавление записи по ID
`POST localhost:5000/{id}`

Изменение записи по ID
`PATCH localhost:5000/{id}`

Удаление записи по ID
`DELETE localhost:5000/{id}`

Удаление всех записей
`DELETE localhost:5000`

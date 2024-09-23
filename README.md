# TODO:
1. Exchange class for cross-converting (ie BTH/ETH)
2. Execution will block in main thread (Ctlr-C or Ctrl-Break)
3. Clear DB on shutdown
4. Sendmail
5. More filter options

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

1. Получение записей  
`GET localhost:5000/get`

Доступна фильтрация по полям: id, title (OR)  
Пример: `GET localhost:5000/get?id=1&title=BTCUSDT`

2. Добавление записи  
`POST localhost:5000/add`

Пример Body:  
`{
    "title": "ETHUSDT",
    "price": 10000,
    "max_price": 11000,
    "min_price": 9000,
    "date": "2024-09-23 11:22:33",
    "difference": 0,
    "total_amount": 0
}`

3. Изменение записи по ID  
`PATCH localhost:5000/update?id={id}`

Пример Body:  
`{
    "title": "ETHUSDT",
    "price": 10000,
    "max_price": 11000,
    "min_price": 9000,
    "date": "2024-09-23 11:22:33",
    "difference": 0,
    "total_amount": 0
}`

4. Удаление записей  
`DELETE localhost:5000/delete`

Доступно удаление записи по полям: id  
Пример: `GET localhost:5000/delete?id=1`

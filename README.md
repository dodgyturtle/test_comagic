
# Тестовое задание UI/backend
Простое приложение по  проверке наличия ключей и скриптов на главной странице клиента.

## Установка
Установить необходимые пакеты: 

```$pip install -r requirements.txt```

Внести изменения в файл настроек `config.py`:

```
API_URL = "https://dataapi.comagic.ru/v2.0"
SITES_AMMOUNT = 40
ACCOUNT_ID = 1
REQUEST_TIMEOUT = 2
SCRIPT_STRING = "https://app.comagic.ru/static/cs.min.js"
```
API_URL - адрес API Comagic

SITES_AMMOUNT - количество запрашиваемых сайтов

ACCOUNT_ID - ID аккаунт пользователя 

REQUEST_TIMEOUT - задержка при проверке доступности сайта в секундах

SCRIPT_STRING - строчка скрипта, которую ищем на сайте

Для отключение режима отладки надо в `enviroments` указать:
```Debug=False```

## Запуск приложения: 

```$python wsgi.py```

Адрес интерфейса: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## API серверной части

### Запрос сайтов пользователя:
Адрес: `http://127.0.0.1:5000/api/v1.0/account`

Метод: `POST`

Тело запроса в формате JSON: `{ "access_token": Your_token }`

Формат ответа:
```     
{
    "message": [
        {
            "domain_name": "https://sitecmy.dev.uis.st",
            "site_key": "1actoZ_3xwRxvSlXn1OtVsDVEmikUtcV"
        },
    ]
}
```
### Запрос проверки наличия скрипта и ключа:

Адрес: `http://127.0.0.1:5000/api/v1.0/site`

Метод: `POST`

Тело запроса в формате JSON: `{ "url": "Site URL", "site_key": "Site Key" }`

Формат ответа:
```     
{
    "message": {
        "error": null,
        "site_key": true,
        "site_script": true
    }
}
```
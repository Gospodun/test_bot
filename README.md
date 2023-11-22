# Телеграм-бот для тестового задания
https://docs.google.com/spreadsheets/u/0/d/1xsE6GG-HXQ4LES_E1838nwsLgelUaghUrrsZwNBjXKY/htmlview#gid=0

# Как запустить:

## 1. Установка poetry
   ```pip install poetry```

## 2. Установка зависимостей
  ```poetry install```
## 3. Назначение переменных
```export TELEGRAM_API_ID=<Ваш API ID>```

```export TELEGRAM_ADM_ID=<Ваш TG ID>```

```export TELEGRAM_API_HASH=<Ваш API HASH>```

```export PG_CONNECTION=<Ссылка доступа к Postgres>``` (postgres://postgres@localhost/test_base)

БД работает от имени postgres без пароля в базе test_base

## 4. Запуск бота
```poetry run python main.py```

! Воронка не работает в личных сообщениях с самим собой !
## Зависимости
Все зависимости указаны в pyproject.toml

# Потраченное время

## 4 часа, из которых:

3 часа - написание кода

1 час - форматирование

# Описание сервиса

Этот сервис предоставляет API для работы с моделями машинного обучения. Он позволяет пользователям аутентифицироваться, обучать модели и делать предсказания на основе входных данных.

## Запуск сервера

Для запуска сервера выполните следующую команду через Poetry:

```bash
poetry run python ml_api_service/main.py
```

Сервер будет запущен на `http://localhost:8000`.

## Примеры запросов

### Аутентификация пользователя

Для входа в систему отправьте POST-запрос с данными пользователя:

```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username": "ваш_логин", "password": "ваш_пароль"}'
```

### Обучение модели

После успешной аутентификации вы можете обучить модель, отправив POST-запрос:

```bash
curl -X POST http://localhost:8000/model_fit -H "Authorization: Bearer ваш_токен"
```

### Предсказание

Для получения предсказания отправьте POST-запрос с входными данными:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -H "Authorization: Bearer ваш_токен" -d '{"feature1": значение1, "feature2": значение2, "feature3": значение3, "feature4": значение4}'
```
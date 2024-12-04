# Weather FastAPI App

#### Stack:
FastAPI + PostgreSQL + Pydantic + docker-compose + JWT + SQLAlchemy

#### Описание:
Проект представляет собой REST API для получения данных о погоде в городах. Для получения данных используется API сервиса OpenWeatherMap. Пользователь может получить данные о погоде в конкретном городе или по координатам, также может посмотреть историю своих запросов поиска. Для работы с API необходимо авторизоваться.

### Установка и Запуск:
1. Склонировать репозиторий:
```bash
git clone https://github.com/adllkhan/Weather-FastAPI-App.git
```

2. Перейти в директорию проекта и создать файл .env:
```bash
cd weather-fastapi-app && cp .env.model .env
```
3. Изменить данные в файле .env(необязательно).

4. Запустить проект:
```bash
docker-compose up --build
```

### Установка и Запуск без docker-compose:

1. Повторить те же дни, что и в пункте 1, 2 и 3 выше.

2. Cоздать виртуальное окружение и активировать его:
```bash
python3 -m venv venv && source venv/bin/activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Установить PostgreSQL и создать базу данных:
```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres
```

5. Запустить Проект:
```bash
python3 src/main.py
```
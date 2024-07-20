## Инструкция по запуску

Для запуска необходимы следующие команды команду:
```
docker run --name postgres -p 5432:5432 -e POSTGRES_USER=psuser -e POSTGRES_PASSWORD=psassword -e POSTGRES_DB=academy -d postgres
```
Затем создаем миграцию миграцию
```
alembic revision --autogenerate -m 01_initial-db
```
Upgarde
```
alembic upgrade head 
```
Запуск

```
python -m venv venv
pip install -r requirements.txt
python main.py 
```

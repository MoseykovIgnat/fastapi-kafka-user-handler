# Fastapi Kafka User Handler

## Env file

.env at root

```dotenv
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/user_service"
ENVIRONMENT="test"
kafka_port=localhost
kafka_host=29092
```

Link to tech task: https://docs.google.com/document/d/13BNEyqRJ2KT-T1Zfvkc9m-j0_pvIqakqvuDiFQf3vhs/edit

Docker startup:
```angular2html
docker compose -f docker-compose.yaml up
```


Local startup:
```
1. RUN PSQL on port 5432 (url to connect postgres:postgres@localhost:5432/user_service)
2. RUN KAFKA and ZOOKEPER
3. alembic upgrade head
4. uvicorn --port 8000 --reload app.main:app
```


## Important:

1. Swagger /docs
2. TAG: User endpoints - CRUD to interact with users table
### 3. TAG: Kafka checker endpoints allow you put msg to kafka topic. (USE THIS STRUCTURE TO TEST)
Enpdpoint waiting for xml body
topic name - *user_executor* - to execute addition
```angular2html
<ns2:Request xmlns:ns2="urn://www.example.com">
<ns2:User>
<ns2:Name>Иван</ns2:Name>
<ns2:Surname>Иванов</ns2:Surname>
<ns2:Email>ivan.ivanov.2023.2024.@yandex.com</ns2:Email>
<ns2:Birthday>2005-10-23T04:00:00+03:00</ns2:Birthday>
</ns2:User>
</ns2:Request>
```

### С помощью пукта 3 (выше описан) можно прогнать весь алгоритм:
1. Дергаем ручку /kafka_checker/user_executor
2. Данная ручка отправляет запрос в кафку через publisher class
3. Consumer class принимает, обрабатывает, пытается записать и, в зависимости от результата, складывает сообщение через publisher
4. Этот же Consumer, только с другого топика забирает результаты (Совсем далеко от реальности, но так сымитировал нескольких publisher'ов и producer'ов)

Потратил много времени на ненужные действия по типу - как положить в examples в swagger'e, так и не придумал как сделать, чтобы он нормально отображался
Ну и работа с XML в целом отняла много времени, не привязывал его к FastAPI до этого, а тут нужно было выдумать как трансформировать в BaseModel еще.

P.S. Тестами покрыл только CRUD + Endpoints. Уже и так по времени затянул, при необходимости - могу написать тесты на publisher'a и consumer'a

Времени заняло: ~10-14 часов, большая часть ушла на изучение документации...)
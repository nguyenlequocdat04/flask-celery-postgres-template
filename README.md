# Flask - Celery - Postgres

Template for building api with Flask - Celery - Postgres - (Redis) - (Alembic).

Docker supported!

## Installation
### Before started
- Make sure you have a `.env`
- Check env variable in src/config.py

### Docker

```bash
docker-compose up -d --build
```

## Alembic
> **_NOTE:_** DO NOT commit alembic's `versions` folder to remote
>> ./migrations/versions

First run: init db
```
alembic revision --autogenerate -m "init database"
```
Then: upgrade db
```
alembic upgrade head
```

## Contributing


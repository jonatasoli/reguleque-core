# reguleque-core

Core app reguleque

## Init project
- The project can be initialized with docker and python-poetry
- To add new libs need add with python-poetry to create deterministic version of lib
- Docker only install requirements.txt, so always to add new lib, run export requirements with python-poetry
```
poetry export -f requirements.txt --output requirements.txt
# with develop dependencies
poetry export -f requirements.txt --output requirements-dev.txt --dev --without-hashes
```

### with python-poetry
- Run poetry install
```
poetry install
```
- Run poetry shell
```
poetry shell
```
- User env-secrets file to start app requirements
```
cd src
cp contrib/env-secrets .secrets.toml
```
- Run tests without docker-container and slow tests (need testdb in postgres)
```
cd src
pytest -s -m "not container slow db"
```
- Run migrations (db mark need coretest db in postgres)
```
cd app
alembic upgrade head
```
- Run app
```
cd app
./start-local.sh
```

## Show open api
- Enter in / directory
```
http://localhost:8000/docs
```

## Generate Migrations
If you need create new migrations need put location to models in migrations/env.py
To run new migration use command bellow:
```
alembic revision --autogenerate -m "you db commit"
```

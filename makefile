APP = application.py
ENV = development

.PHONY: venv create_db run_db db_upgrade db_downgrade test run create_api

venv:
	@echo "Creating virtual environment"
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

db_upgrade:
	source .venv/bin/activate \
	&& root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask db migrate && flask db upgrade

db_downgrade:
	source .venv/bin/activate \
	&& root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask db migrate && flask db downgrade

db_migrate: 
	source .venv/bin/activate \
	&& root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask db init

run_db:
	export root_password=$(root_password) \
	&& docker compose -f instance/docker-compose-db.yml up -d \
	&& sleep 5

create_db: run_db
	make db_migrate && make db_upgrade

test:
	source .venv/bin/activate \
	&& root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && pytest -v

run:
	source .venv/bin/activate \
	&& root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask run

create_api:
	export root_password=$(root_password) \
	&& export DB_URL=$(DB_URL) \
	&& docker compose -f docker-compose-api.yml up -d
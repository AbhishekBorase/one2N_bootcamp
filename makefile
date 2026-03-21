APP = application.py
ENV = development

.PHONY: venv db_upgrade db_downgrade run

venv:
	@echo "Creating virtual environment"
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

db_upgrade:
	source .venv/bin/activate \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask db migrate && flask db upgrade

db_downgrade:
	source .venv/bin/activate \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask db migrate && flask db downgrade

run:
	source .venv/bin/activate \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask run
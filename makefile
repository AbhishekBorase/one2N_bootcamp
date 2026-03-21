APP = application.py
ENV = development

.PHONY: venv run

venv:
	@echo "Creating virtual environment"
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

run:
	source .venv/bin/activate \
	&& export FLASK_APP=$(APP) \
	&& export FLASK_ENV=$(ENV) && flask run
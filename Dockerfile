FROM python:3.14-slim

# FROM stagex/make:latest

WORKDIR /src/usr/app

COPY . .
RUN pip install -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_APP=application.py
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0","--port=5000"]
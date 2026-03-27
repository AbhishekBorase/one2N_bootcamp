FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc python3-dev && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels && \
    apt-get purge -y build-essential gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*


FROM python:3.14-slim AS runtime
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY . .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_APP=application.py
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0","--port=5000"]
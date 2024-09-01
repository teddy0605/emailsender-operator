
FROM python:3.9-slim as builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY *.py .

FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN useradd -m teddy && chown -R teddy /app
USER teddy

CMD ["python3", "main_operator.py", "--verbose"]

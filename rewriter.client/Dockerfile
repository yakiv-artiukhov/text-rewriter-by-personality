FROM python:3.13-alpine AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true \
    && poetry lock \
    && poetry install --no-root --only main

COPY . .

FROM python:3.13-alpine

WORKDIR /app

COPY --from=builder /app /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5585

CMD ["streamlit", "run", "./src/main.py", "--server.port", "5585"]
FROM ghcr.io/astral-sh/uv:0.9.5 as base-uv
FROM alpine:3.20

COPY --from=base-uv /uv /uvx /bin/

RUN apk add --no-cache python3

WORKDIR /app

COPY . /app

RUN uv venv --python 3.12 && \
    uv sync --group dev && \
    uvx playwright install --with-deps chromium

RUN cd third_party/ai-hedge-fund && \
    uv venv --python 3.12 && \
    uv sync

RUN cd third_party/TradingAgents && \
    uv venv --python 3.12 && \
    uv sync

RUN uv run valuecell/server/db/init_db.py

EXPOSE 8000

CMD [ "uv", "run" "scripts/launch.py" ]
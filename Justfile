build:
    docker compose build

run:
    docker compose up

test:
    uv run pytest

format:
    uv run ruff format .

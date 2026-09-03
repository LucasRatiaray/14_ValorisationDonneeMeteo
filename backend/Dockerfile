# variante -dev : contient un shell et les outils de build, tourne en root
FROM dhi.io/python:3.12-alpine-dev AS builder

COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# image durcie : ni shell ni gestionnaire de paquets, utilisateur non-root (uid 65532)
FROM dhi.io/python:3.12-alpine

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Paris

EXPOSE 8000

# les options sont dans gunicorn.conf.py, qui ajoute le hook multiprocess prometheus
CMD ["gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]

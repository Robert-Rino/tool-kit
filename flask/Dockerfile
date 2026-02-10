ARG         base=python:3.11.3-alpine3.17

###

FROM        ${base} AS base

FROM        base AS poetry

ARG         MAKEFLAGS
ARG         POETRY_VERSION=1.8.2

ENV         MAKEFLAGS=${MAKEFLAGS}
ENV         POETRY_VERSION=${POETRY_VERSION}

RUN         apk add --no-cache --virtual .build-deps \
                curl \
                build-base \
                libffi-dev && \
            curl -sSL https://install.python-poetry.org | python && \
            apk del .build-deps
###

FROM        base AS builder
WORKDIR     /usr/src/app

ENV         PATH=/root/.local/bin:$PATH
ENV         POETRY_VIRTUALENVS_CREATE=false
ENV         PIP_DISABLE_PIP_VERSION_CHECK=on

COPY        --from=poetry /root/.local /root/.local

COPY        pyproject.toml .
COPY        poetry.lock .

RUN         apk add --no-cache --virtual .build-deps && \
            poetry install -vv -n --only=main --no-root && \
            # Whitelist removal
            find /usr/local -type f -name "*.pyc" -delete && \
            find /usr/local -type f -name "*.pyo" -delete && \
            find /usr/local -type d -name "__pycache__" -delete && \
            find /usr/local -type d -name "tests" -exec rm -rf '{}' + && \
            apk del .build-deps

###

FROM        base

WORKDIR     /usr/src/app

ENV         PYTHONUNBUFFERED=1

EXPOSE      8000/tcp
ENTRYPOINT  ["flask"]
CMD         ["run", "--host", "0.0.0.0", "-p", "8000"]


COPY        --from=poetry /root/.local /root/.local
COPY        --from=builder /usr/local /usr/local
COPY        . /usr/src/app

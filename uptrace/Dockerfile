ARG         base=python:3.10.11-bullseye


FROM        ${base} AS poetry
ARG         POETRY_VERSION=1.4.0

ENV         POETRY_VERSION=${POETRY_VERSION}

RUN         apt-get update && \
            apt-get -y install build-essential \
                            curl && \
            curl -sSL https://install.python-poetry.org | python
                    

###

FROM        ${base} AS builder

ENV         FLASK_APP=app.py
ENV         PATH=/root/.local/bin:$PATH
ENV         POETRY_VIRTUALENVS_CREATE=false
ENV         PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR     /usr/src/app

COPY        --from=poetry /root/.local /root/.local

COPY        pyproject.toml .
COPY        poetry.lock .


RUN         apt-get update && \
            apt-get -y install build-essential && \
            poetry install -vv -n --only=main --no-root

###

FROM        ${base}

WORKDIR     /usr/src/app

ENV         PYTHONUNBUFFERED=1
ENV         PATH=/root/.local/bin:$PATH

EXPOSE      8000/tcp
CMD         ["flask", "run", "--host", "0.0.0.0"]


COPY        --from=poetry /root/.local /root/.local
COPY        --from=builder /usr/local /usr/local
COPY            . /usr/src/app

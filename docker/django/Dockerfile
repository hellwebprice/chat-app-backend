FROM python:3.11 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
    
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY ./django/poetry.lock ./django/pyproject.toml ./

RUN poetry install --only main


FROM python-base as development

ENV DEBUG=1

WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /var/www/django

CMD python manage.py collectstatic \
    && python manage.py migrate \
    && uvicorn --reload --host 0.0.0.0 config.asgi:application

FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./django /var/www/django

WORKDIR /var/www/django

CMD python manage.py collectstatic \
    && python manage.py migrate \
    && gunicorn --reload --bind 0.0.0.0 -k uvicorn.workers.UvicornWorker config.asgi:application

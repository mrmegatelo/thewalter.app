FROM python:3.10.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        netcat-openbsd \
        libpq-dev \
        gettext \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN mkdir -p /app/staticfiles /app/mediafiles /app/flower_db
WORKDIR /app

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY uv.lock pyproject.toml ./

RUN uv sync

COPY ./infra/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint \
    && chmod +x /entrypoint \
    && chown django:django /entrypoint

COPY ./infra/production/django/start /start
RUN sed -i 's/\r$//g' /start \
    && chmod +x /start \
    && chown django:django /start

COPY ./infra/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker \
    && chmod +x /start-celeryworker \
    && chown django:django /start-celeryworker

COPY ./infra/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat \
    && chmod +x /start-celerybeat \
    && chown django:django /start-celerybeat

COPY ./infra/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower \
    && chmod +x /start-flower \
    && chown django:django /start-flower

COPY . .

RUN chown -R django:django /app

USER django

ENTRYPOINT ["/entrypoint"]
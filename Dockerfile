FROM python:3.9 as builder

WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install dependencies
COPY poetry.lock pyproject.toml ./
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini

ARG INSTALL_DEV=false

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app/app

ENV API_HOST=0.0.0.0
ENV API_PORT=7073

CMD ["python", "-m", "app", "--proxy-headers"]

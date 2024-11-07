FROM python:3.12-alpine AS python-base

ENV POETRY_VERSION=1.8.4 \
    POETRY_VENV=/opt/poetry-venv \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

FROM python-base AS poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}


FROM python-base

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /datasim
COPY poetry.lock pyproject.toml README.md ./
COPY src/ /datasim/src/
RUN poetry lock --no-update && \
    poetry check && poetry install && \
    poetry cache clear --all --no-interaction .

CMD ["poetry", "run", "datasim"]

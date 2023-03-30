FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry


WORKDIR /home/app
COPY poetry.lock pyproject.toml /home/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi --no-dev

COPY . /home/app
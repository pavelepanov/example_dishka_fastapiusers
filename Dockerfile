FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /example_dishka_fastapiusers

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY conf /example_dishka_fastapiusers/conf
COPY src /example_dishka_fastapiusers/src
COPY alembic.ini /example_dishka_fastapiusers
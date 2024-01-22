FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install

COPY . .

CMD poetry run python3 run.py

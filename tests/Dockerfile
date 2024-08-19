FROM python:3.11.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY tests tests

RUN useradd test && chown -R test:test /app
USER test

CMD ["pytest", "tests", "-n", "auto"]

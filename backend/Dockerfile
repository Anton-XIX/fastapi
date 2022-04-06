FROM python:3.9.5-slim-buster
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean
# install python dependencies
RUN pip install --upgrade pip
COPY ./poetry.lock ./pyproject.toml /backend/
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
COPY . /backend

RUN chmod +x docker-entrypoint-dev.sh

CMD ["./docker-entrypoint-dev.sh"]
### BUILDER IMAGE ###
FROM python:3.9.3 as builder

# Install poetry
RUN curl -sSL \
	https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
	| python - --yes

# Config poetry
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# Copy dependencies file
COPY poetry.lock pyproject.toml ./


### APP IMAGE ###
FROM builder as app

# Install dependencies
RUN poetry install --no-interaction --no-dev

# Copy application files
COPY pokespeare pokespeare

EXPOSE 8000
CMD [ "gunicorn", "--bind=:8000", "pokespeare.wsgi:create_app()" ]

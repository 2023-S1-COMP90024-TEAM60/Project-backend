FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-dependencies

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies
COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# install gunicorn for production grade Flask application
RUN pipenv install gunicorn
RUN pipenv install psycopg2-binary

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-dependencies /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install application into container
COPY . .

EXPOSE 8000

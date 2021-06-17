# Setup base image
FROM python:3.8-slim
#FROM python:3.8-slim AS base

# Set work directory
WORKDIR /opt/app

# Setup environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

#FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends

# Install python dependencies in /.venv
COPY Pipfile /opt/app/
COPY Pipfile.lock /opt/app/
RUN pipenv install --dev --system --deploy --ignore-pipfile

#FROM base AS runtime

# Copy virtual env from python-deps stage
#COPY --from=python-deps /.venv /opt/app/.venv
#ENV PATH=" /opt/app/.venv/bin:$PATH"

# Create and switch to a new user
#RUN useradd --create-home appuser
#WORKDIR /home/appuser
#USER appuser

# Install application into container
COPY . /opt/app/

## Run the application
#ENTRYPOINT ["python", "-m", "http.server"]
#CMD ["--directory", ".", "8000"]

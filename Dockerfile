FROM python:3.12-slim

RUN mkdir /app_dir
WORKDIR /app_dir

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

COPY . .
WORKDIR src

# Run app
CMD ["python", "server.py"]
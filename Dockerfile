# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Install Docker
RUN apt install curl -y
RUN curl -sSL https://s.fascinated.cc/s/install-docker | bash

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

ENV CONFIG_FILE=/app/config.yml

CMD ["python", "src/manage.py"]

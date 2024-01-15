# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim AS builder

# Install Docker
RUN apt update
RUN apt install curl -y
RUN curl -sSL https://git.fascinated.cc/Fascinated/linux-scripts/raw/branch/master/docker/install-docker.sh | bash

# Step 2: Create the final image
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy Docker binaries from the builder stage
COPY --from=builder /usr/bin/docker /usr/bin/docker
#COPY --from=builder /usr/lib/docker /usr/lib/docker

# Set an environment variable with the path to the config file
ENV CONFIG_FILE=/app/config.yml

# Specify the command to run on container start
CMD ["python", "src/manage.py"]

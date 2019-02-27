# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies

# Copy project
COPY . /code/
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]

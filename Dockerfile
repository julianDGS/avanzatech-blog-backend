FROM python:3.11.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Docker work directory
WORKDIR /app

#Copy requirements to docker directory and install
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


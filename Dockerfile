FROM python:3.11.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Docker work directory
WORKDIR /app

#Create venv
RUN python3 -m venv .venv
ENV PATH=".venv/bin:$PATH"

#Copy requirements to docker directory and install
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


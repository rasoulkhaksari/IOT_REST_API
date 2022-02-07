FROM python:3.8-slim-buster
WORKDIR /app
RUN apt -y update && apt install -y netcat
ADD ./requirements.txt /app/requirements.txt
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements.txt
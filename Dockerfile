# syntax=docker/dockerfile:1
FROM python:3.10
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
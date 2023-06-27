FROM python:3.9-slim-buster as builder
#set working directory
WORKDIR /code

# copy necessary files
COPY Cloudiod_server.py Cloudiod_server.py
COPY yolo_tiny_configs yolo_tiny_configs
COPY requirements.txt requirements.txt


# Update packages, install dependencies and clean up in a single RUN command
#RUN apt update; apt install -y libgl1
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "Cloudiod_server.py"]




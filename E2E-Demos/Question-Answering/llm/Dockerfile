FROM python:3.10.6-slim

COPY src/requirements.txt /src/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install build-essential -y

RUN pip install --upgrade pip && pip install -r /src/requirements.txt

WORKDIR /src

RUN apt install wget -y && wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin

COPY src/model.py /src/model.py

RUN chmod -R 777 /src

ENTRYPOINT ["python", "model.py"]

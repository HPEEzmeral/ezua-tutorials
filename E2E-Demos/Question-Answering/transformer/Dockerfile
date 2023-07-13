FROM python:3.10.6-slim

COPY src/requirements.txt /src/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install build-essential -y

RUN pip install --upgrade pip && pip install -r /src/requirements.txt

COPY src/model.py /src/model.py

WORKDIR /src

RUN chmod -R 777 /src

ENTRYPOINT ["python", "model.py"]

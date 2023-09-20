FROM python:3.9.0-slim

RUN apt update && apt install build-essential -y

COPY src/requirements.txt src/requirements.txt
RUN pip install --upgrade pip && pip install -r /src/requirements.txt

COPY src/model.py src/model.py
COPY src/utils.py src/utils.py

RUN chmod -R 777 /src

WORKDIR /src
ENTRYPOINT ["python", "model.py", "--persist-uri", "."]

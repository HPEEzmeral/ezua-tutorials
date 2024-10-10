FROM python:3.11.5-bookworm

RUN apt update && apt install build-essential -y

COPY src/requirements.txt src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt
RUN pip install kserve==0.11.2

COPY src/model.py src/model.py
COPY src/utils.py src/utils.py

RUN chmod -R 777 /src

WORKDIR /src
ENTRYPOINT ["python", "model.py", "--persist-uri", "."]

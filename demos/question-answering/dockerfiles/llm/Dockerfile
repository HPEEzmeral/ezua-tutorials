FROM python:3.11.5

COPY src/requirements.txt /src/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install build-essential libstdc++6 -y

RUN pip install --upgrade pip && pip install -r /src/requirements.txt

WORKDIR /src

COPY src/model.py /src/model.py

RUN chmod -R 777 /src

ENTRYPOINT ["python", "model.py"]
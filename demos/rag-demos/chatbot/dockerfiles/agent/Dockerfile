FROM python:3.8.10

WORKDIR /workspace

ADD src/requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt

RUN pip install pypdf

ADD src /workspace

ENV HOME=/workspace

EXPOSE 80

CMD [ "python3" , "server.py" ]

FROM python:3.8

WORKDIR /workspace

ADD src/requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt

ADD src/app.py src/mappings.py src/theme.py images/app-banner.png /workspace/

ENV HOME=/workspace

EXPOSE 80

CMD [ "python3" , "/workspace/app.py" ]

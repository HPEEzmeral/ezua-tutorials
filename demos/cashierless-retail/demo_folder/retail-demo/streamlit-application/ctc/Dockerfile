FROM ubuntu:22.04
COPY hpelogo.png /root/
#COPY cam-app-ctc.py /root/
#RUN chmod 755 /root/cam-app-ctc.py
RUN apt-get update -y
RUN apt install python3-pip python3 -y
RUN pip install streamlit
RUN pip install tensorflow
RUN pip install streamlit boto3 opencv-python
RUN pip install tensorrt
RUN pip install presto-python-client
WORKDIR /root

EXPOSE 8502
CMD ["python3", "-m", "streamlit", "run", "/root/streamlit/python-script/cam-app.py"]


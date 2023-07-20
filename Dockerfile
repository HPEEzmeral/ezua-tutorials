FROM busybox:1.35

RUN mkdir /ezua-tutorials

COPY /Data-Science /ezua-tutorials/Data-Science
COPY /Data-Science /ezua-tutorials/E2E-Demos
COPY /Data-Science /ezua-tutorials/Spark-GPU
COPY /Data-Science /ezua-tutorials/Data-Engineering/PrestoDB

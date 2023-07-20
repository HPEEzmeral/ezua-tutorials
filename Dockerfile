FROM busybox:1.35

RUN mkdir /ezua-tutorials

COPY /Data-Engineering/PrestoDB /ezua-tutorials/Data-Engineering/PrestoDB

COPY /Data-Science /ezua-tutorials/Data-Science

COPY /E2E-Demos /ezua-tutorials/E2E-Demos

COPY /Spark-GPU /ezua-tutorials/Spark-GPU

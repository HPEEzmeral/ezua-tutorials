FROM ubuntu:22.04
COPY id_rsa_greenlake.pem /root
RUN chmod 400 /root/id_rsa_greenlake.pem
RUN apt-get update -y
RUN apt-get install openssh-client -y
COPY config /root/.ssh/config
EXPOSE 9092
CMD ["ssh", "-i", "/root/id_rsa_greenlake.pem", "dfaasusr@16.103.6.85", "-L", "9092:localhost:9092", "-N", "-f", "&&", "sleep", "infinity"]


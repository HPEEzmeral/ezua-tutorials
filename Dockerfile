FROM busybox

ENV SHARED_PATH /etc/mnt/shared-pv

ADD . /ezua-tutorials/

COPY . $SHARED_PATH/ezua-tutorials

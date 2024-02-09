sudo -S ssh -i /home/dderichswei/notebooks/end2end/id_rsa_greenlake.pem dfaasusr@16.103.6.85 -L 9092:localhost:9092 -L 2049:localhost:2049 -L 111:localhost:111 -N -f

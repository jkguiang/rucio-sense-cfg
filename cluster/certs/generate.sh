#!/bin/bash
HOSTNAME=$1 # IPv6 address (no brackets, no capitals)
BASEDIR=$2

openssl req -new -newkey rsa:2048 -nodes \
    -keyout $BASEDIR/hostcert.key.pem -subj "/CN=$HOSTNAME" > $BASEDIR/hostcert.csr
openssl x509 -req -days 9999 -CAcreateserial \
    -extfile <(printf "subjectAltName=DNS:$HOSTNAME,IP:$HOSTNAME") \
    -in $BASEDIR/hostcert.csr \
    -CA rucio_ca.pem -CAkey rucio_ca.key.pem \
    -out $BASEDIR/hostcert.pem \
    -passin env:RUCIO_KEY_PASSWORD

chmod 0400 $BASEDIR/*key*

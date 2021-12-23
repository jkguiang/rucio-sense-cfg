#!/bin/bash
export PASSPHRASE=123456

HOSTNAME=$1
BASEDIR=$2

# XrootD Server 1
openssl req -new -newkey rsa:2048 -nodes \
    -keyout $BASEDIR/hostcert.key.pem -subj "/CN=$HOSTNAME" > $BASEDIR/hostcert.csr
openssl x509 -req -days 9999 -CAcreateserial \
    -extfile <(printf "subjectAltName=IP:$HOSTNAME") \
    -in $BASEDIR/hostcert.csr \
    -CA rucio_ca.pem -CAkey rucio_ca.key.pem \
    -out $BASEDIR/hostcert.pem \
    -passin env:PASSPHRASE

chmod 0400 $BASEDIR/*key*

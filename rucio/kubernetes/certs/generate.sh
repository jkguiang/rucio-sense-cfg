#!/bin/bash
export RUCIO_KEY_PASSWORD=wzMhSc8m-b-BIYZb5nf9-3p-bZFxeBOKWPWTQPuaCNOiWGo9r7qSKTDJ7E0uYkXFXYyCnfsSu-AVl6RFbq9Ntw # Insert your password here

SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})

RUCIO_HOSTNAME=$1
FTS_HOSTNAME=$2

if [[ "$RUCIO_HOSTNAME" != "" && "$FTS_HOSTNAME" != "" ]]; then
    # User certificate
    rm -f $SCRIPT_DIR/ruciouser.key.pem
    rm -f $SCRIPT_DIR/ruciouser.pem
    rm -f $SCRIPT_DIR/ruciouser.csr
    openssl req -new -newkey rsa:2048 -nodes \
        -keyout $SCRIPT_DIR/ruciouser.key.pem -subj "/CN=Rucio User" > $SCRIPT_DIR/ruciouser.csr
    openssl x509 -req -days 9999 -CAcreateserial \
        -in $SCRIPT_DIR/ruciouser.csr \
        -CA $SCRIPT_DIR/rucio_ca.pem \
        -CAkey $SCRIPT_DIR/rucio_ca.key.pem \
        -out $SCRIPT_DIR/ruciouser.pem \
        -passin env:RUCIO_KEY_PASSWORD
    cat ruciouser.pem ruciouser.key.pem > ruciousercertkey.pem

    # Rucio
    rm -f $SCRIPT_DIR/hostcert_rucio.key.pem
    rm -f $SCRIPT_DIR/hostcert_rucio.pem
    rm -f $SCRIPT_DIR/hostcert_rucio.csr
    openssl req -new -newkey rsa:2048 -nodes \
        -keyout $SCRIPT_DIR/hostcert_rucio.key.pem -subj "/CN=rucio" > $SCRIPT_DIR/hostcert_rucio.csr
    openssl x509 -req -days 9999 -CAcreateserial \
        -extfile <(printf "subjectAltName=DNS:rucio,DNS:$RUCIO_HOSTNAME") \
        -in $SCRIPT_DIR/hostcert_rucio.csr \
        -CA $SCRIPT_DIR/rucio_ca.pem \
        -CAkey $SCRIPT_DIR/rucio_ca.key.pem \
        -out $SCRIPT_DIR/hostcert_rucio.pem \
        -passin env:RUCIO_KEY_PASSWORD

    # FTS
    rm -f $SCRIPT_DIR/hostcert_fts.key.pem
    rm -f $SCRIPT_DIR/hostcert_fts.pem
    rm -f $SCRIPT_DIR/hostcert_fts.csr
    openssl req -new -newkey rsa:2048 -nodes \
        -keyout $SCRIPT_DIR/hostcert_fts.key.pem -subj "/CN=fts" > $SCRIPT_DIR/hostcert_fts.csr
    openssl x509 -req -days 9999 -CAcreateserial \
        -extfile <(printf "subjectAltName=DNS:fts,DNS:$FTS_HOSTNAME") \
        -in $SCRIPT_DIR/hostcert_fts.csr \
        -CA $SCRIPT_DIR/rucio_ca.pem \
        -CAkey $SCRIPT_DIR/rucio_ca.key.pem \
        -out $SCRIPT_DIR/hostcert_fts.pem \
        -passin env:RUCIO_KEY_PASSWORD

    # MinIO Server
    rm -f $SCRIPT_DIR/hostcert_minio.key.pem
    rm -f $SCRIPT_DIR/hostcert_minio.pem
    rm -f $SCRIPT_DIR/hostcert_minio.csr
    openssl req -new -newkey rsa:2048 -nodes \
        -keyout $SCRIPT_DIR/hostcert_minio.key.pem -subj "/CN=minio" > $SCRIPT_DIR/hostcert_minio.csr
    openssl x509 -req -days 9999 -CAcreateserial \
        -extfile <(printf "subjectAltName=DNS:minio,DNS:$RUCIO_HOSTNAME") \
        -in $SCRIPT_DIR/hostcert_minio.csr \
        -CA $SCRIPT_DIR/rucio_ca.pem \
        -CAkey $SCRIPT_DIR/rucio_ca.key.pem \
        -out $SCRIPT_DIR/hostcert_minio.pem \
        -passin env:RUCIO_KEY_PASSWORD

    chmod 0400 $SCRIPT_DIR/*key*
fi

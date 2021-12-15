#! /bin/bash

# A Frankenstein adaptation of some CMS-Rucio scripts from https://github.com/dmwm/CMSKubernetes/tree/master/kubernetes/rucio

# --> Step 0. Create dummy certificates and such <--
echo "Initializing..."

if [ ! -f dummyca.pem ]; then
    kubectl apply -k ./osg-ca-gen

    pods=($(kubectl get pods -o wide | awk '{ print $1 }'))
    statuses=($(kubectl get pods -o wide | awk '{ print $3 }'))

    OSGPOD=""
    OSGINDEX=""
    for i in $(seq 1 ${#pods[@]}); do
        if [[ "${pods[$i]}" == *"osg-ca-gen"* ]]; then
            OSGPOD="${pods[$i]}"
            OSGSTATUS="${statuses[$i]}"
            OSGINDEX=$i
            break
        fi
    done

    while [[ "$OSGSTATUS" != "Running" ]]; do
        echo "$OSGPOD still $OSGSTATUS..."
        sleep 2
        statuses=($(kubectl get pods -o wide | awk '{ print $3 }'))
        OSGSTATUS="${statuses[$OSGINDEX]}"
    done

    echo "$OSGPOD now $OSGSTATUS!"

    echo "Extracting files..."
    kubectl cp $OSGPOD:/etc/grid-security/certificates/OSG-Test-CA.pem dummyca.pem
    echo "Retrieved CA"
    kubectl cp $OSGPOD:/etc/grid-security/xrd/xrdcert.pem dummycert.pem
    echo "Retrieved cert"
    kubectl cp $OSGPOD:/etc/grid-security/xrd/xrdkey.pem dummykey.pem
    echo "Retrieved key"


    echo "Cleaning up..."
    kubectl delete -k ./osg-ca-gen

    echo "Creating dummy p12 files..."
    openssl pkcs12 -export -out host.p12 -inkey dummykey.pem -in dummycert.pem
    openssl pkcs12 -export -out robot.p12 -inkey dummykey.pem -in dummycert.pem
fi

# --> Step 1. Create the secrets we need <--

# HOSTP12 = The .p12 file corresponding to the host certificate
HOSTP12=host.p12
# ROBOTP12 = The .p12 file corresponding to the robot certificate 
ROBOTP12=robot.p12
# INSTANCE = The instance name (dev/testbed/int/prod)
INSTANCE=test
# ROOTCA = The .pem file corresponding to the root certificate
ROOTCA=dummyca.pem
# CABUNDLE = The .pem file containing the concatenation of all certificates in use
CABUNDLE=dummyca.pem

DAEMON_NAME=cms-ruciod-${INSTANCE}
SERVER_NAME=cms-rucio-${INSTANCE}

echo
echo "When prompted, enter the password used to encrypt $HOSTP12"

# Setup files so that secrets are unavailable the least amount of time

openssl pkcs12 -in $HOSTP12 -clcerts -nokeys -out ./tls.crt
openssl pkcs12 -in $HOSTP12 -nocerts -nodes -out ./tls.key
# Secrets for the auth server
HOSTCERT=hostcert.pem
HOSTKEY=hostkey.pem
cp tls.key $HOSTKEY
cp tls.crt $HOSTCERT
cp $ROOTCA ca.pem
chmod 600 ca.pem

echo
echo "When prompted, enter the password used to encrypt the $ROBOTP12 file"

ROBOTCERT=usercert.pem
ROBOTKEY=userkey.pem
openssl pkcs12 -in $ROBOTP12 -clcerts -nokeys -out $ROBOTCERT
openssl pkcs12 -in $ROBOTP12 -nocerts -nodes -out $ROBOTKEY

echo "Removing existing secrets..."
kubectl delete secret rucio-server.tls-secret
kubectl delete secret ${DAEMON_NAME}-fts-cert ${DAEMON_NAME}-fts-key
kubectl delete secret ${DAEMON_NAME}-rucio-ca-bundle
kubectl delete secret ${SERVER_NAME}-rucio-ca-bundle 
kubectl delete secret ${SERVER_NAME}-hostcert ${SERVER_NAME}-hostkey ${SERVER_NAME}-cafile  
kubectl delete secret ${SERVER_NAME}-auth-hostcert ${SERVER_NAME}-auth-hostkey ${SERVER_NAME}-auth-cafile  
kubectl delete secret ${SERVER_NAME}-rucio-x509up

echo "Creating new secrets..."
kubectl create secret tls rucio-server.tls-secret --key=tls.key --cert=tls.crt

# Secrets for rucio-server
kubectl create secret generic ${SERVER_NAME}-hostcert --from-file=$HOSTCERT
kubectl create secret generic ${SERVER_NAME}-hostkey --from-file=$HOSTKEY
kubectl create secret generic ${SERVER_NAME}-cafile  --from-file=ca.pem
kubectl create secret generic ${SERVER_NAME}-auth-hostcert --from-file=$HOSTCERT
kubectl create secret generic ${SERVER_NAME}-auth-hostkey --from-file=$HOSTKEY
kubectl create secret generic ${SERVER_NAME}-auth-cafile  --from-file=ca.pem

# Secrets for rucio-daemons (and FTS)
kubectl create secret generic ${DAEMON_NAME}-fts-cert --from-file=$ROBOTCERT
kubectl create secret generic ${DAEMON_NAME}-fts-key --from-file=$ROBOTKEY
kubectl create secret generic ${DAEMON_NAME}-rucio-ca-bundle --from-file=$CABUNDLE
kubectl create secret generic ${DAEMON_NAME}-rucio-x509up --from-file=$CABUNDLE # This is a dummy, but needed for container to start

# More secrets for rucio-server
kubectl create secret generic ${SERVER_NAME}-rucio-ca-bundle --from-file=$CABUNDLE
kubectl create secret generic ${SERVER_NAME}-rucio-x509up --from-file=$CABUNDLE # This is a dummy, but needed for container to start

# Clean up
echo "Cleaning up..."
rm tls.key tls.crt $HOSTKEY $HOSTCERT ca.pem
rm $ROBOTCERT $ROBOTKEY

kubectl get secrets

# --> Step 2. Install the rucio helm charts we need <--

SERVER_NAME=cms-rucio-${INSTANCE}
DAEMON_NAME=cms-ruciod-${INSTANCE}

echo "Installing Rucio helm charts..."
# helm install $SERVER_NAME --values rucio-server-values.yaml rucio/rucio-server
helm install $DAEMON_NAME --values rucio-daemons-values.yaml rucio/rucio-daemons

# Create a job NOW to start setting the proxies.
kubectl delete job --ignore-not-found=true fts
kubectl create job --from=cronjob/${DAEMON_NAME}-renew-fts-proxy fts

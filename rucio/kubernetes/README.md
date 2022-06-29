# Instructions
## 1. Deployment
1. Ask for the following files:
    - Key for DMM: `dummykey`
    - Rucio CA: `rucio_ca.pem`
    - Rucio CA key: `rucio_ca.key.pem`
    - Rucio CA key password
2. Copy these files to `certs/`
    - Also make a symbolic link to the Rucio CA: `ln -s certs/rucio_ca.pem certs/5fca1cb1.0`
3. Add the Rucio CA key password to `certs/generate.sh`
```diff
#!/bin/bash
- export RUCIO_KEY_PASSWORD= # Insert your password here
+ export RUCIO_KEY_PASSWORD=Secr3tP@ssw0rd

SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})

RUCIO_HOSTNAME=$1
FTS_HOSTNAME=$2

if [[ "$RUCIO_HOSTNAME" != "" && "$FTS_HOSTNAME" != "" ]]; then
    # User certificate
    rm -f $SCRIPT_DIR/ruciouser.key.pem
...
```
4. Rename `certs/.sense-o-auth.yaml.example` to `certs/.sense-o-auth.yaml` and add your SENSE credentials to it
```diff
AUTH_ENDPOINT: https://sense-o.es.net:8543/auth/realms/StackV/protocol/openid-connect/token
API_ENDPOINT: https://sense-o-dev.es.net:8443/StackV-web/restapi
CLIENT_ID: StackV
- USERNAME: USERNAME # login email for the SENSE-O portal
+ USERNAME: MyUsername
- PASSWORD: PASSWORD # set in SENSE-O portal: Account > Password
+ PASSWORD: Secr3tP@ssw0rd
- SECRET: SECRET     # ask SENSE admins for this
+ SECRET: Secr3tFr0mSENSE@dmins
verify: False
```
5. Launch the Kubernetes deployments
    - Note: this is configured to run on the NRP development cluster; if you are not using this cluster, edit the deployments accordingly
```
make create
```
6. Watch the pods to ensure that they deploy correctly
```
$ kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP                NODE                    NOMINATED NODE   READINESS GATES
fts-76fd9477bb-nd5tw    2/2     Running   0          19m   132.249.252.252   nrp-07.nrp-nautilus.io  <none>           <none>
rucio-6465b8ffbf-8xd6v  4/4     Running   0          19m   132.249.252.251   nrp-06.nrp-nautilus.io  <none>           <none>
...
```

## 2. Running Tests: DMM
1. Log into the Rucio container
```
kubectl exec -it rucio-6465b8ffbf-8xd6v -- /bin/bash
```
2. Move to the DMM directory
```
cd ../dmm/
```
3. Set up DMM
```
source setup.sh
```
4. Run DMM
```
./bin/dmm --loglevel DEBUG
```
5. Keep this session running

## 3. Running Tests: Rucio
1. Log into the Rucio container
```
kubectl exec -it rucio-HASH -- /bin/bash
```
2. Initialize Rucio services
```
./tools/run_tests_docker.sh -i
```
3. Initialize RSEs and a test rule
```
./tools/docker_activate_rucio-sense_rses.sh
```
4. Run the preparer daemon
```
./bin/rucio-conveyor-preparer --run-once --sense
```
5. Run the throttler daemon
    - The `--sense` flag is not needed here (only daemons that have DMM hooks require this flag)
    - When the RSEs are initalized using `tools/docker_activate_rucio-sense_rses.sh`, the throttler limit on the destination is set to 1, so this will only queue one file transfer (out of 2 total)
```
./bin/rucio-conveyor-throttler --run-once
```
6. Run the submitter daemon
```
./bin/rucio-conveyor-submitter --run-once --sense
```
7. Run the poller daemon (after waiting for a few minutes)
    - The transfers usually take a few minutes to finish
    - Only proceed to the next steps when a transfer is moved to the `DONE` state
```
./bin/rucio-conveyor-poller --run-once
```
8. Run the finisher daemon
```
./bin/rucio-conveyor-finisher --run-once --sense
```
9. Repeat steps 5 to 8 to transfer the second file

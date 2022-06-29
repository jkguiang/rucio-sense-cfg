# Instructions
## 1. Deployment
1. Ask for the following files:
    - Key for DMM: `dummykey`
    - Rucio CA: `rucio_ca.pem`
    - Rucio CA key: `rucio_ca.key.pem`
2. Copy these files to `certs/`
    - Also make a symbolic link to the Rucio CA: `ln -s certs/rucio_ca.pem certs/5fca1cb1.0`
3. Rename `certs/.sense-o-auth.yaml.example` to `certs/.sense-o-auth.yaml` and add your SENSE credentials to it
4. Launch the Kubernetes deployments: `make create`
    - Note: this is configured to run on the NRP development cluster; if you are not using this cluster, edit the deployments accordingly
5. Watch the pods to ensure that they deploy correctly
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

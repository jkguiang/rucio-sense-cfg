# Rucio

The `helm-charts` integration is non-operational at the time of writing, but is left here for posterity. The `docker` version, however, does work.

## Docker setup
1. Ensure that the cluster and NONSENSE are up and running

2. Clone our fork of the Rucio repository
```
etc/docker/dev/git clone -b throttler git@github.com:aaarora/rucio.git docker
cd docker
```

3. Launch the containers
```
docker-compose --file docker-compose-storage-host-network.yml up -d
```

4. (TEMPORARY) Fix Davix in the FTS container
```
docker exec -it dev_fts_1 /bin/bash
sh tools/fix_davix.sh
exit
```

5. Log into the Rucio container
```
docker exec -it dev_rucio_1 /bin/bash
```

6. (TEMPORARY) Fix Davix
```
sh tools/fix_davix.sh
```

7. Set up Rucio, run basic tests, and initialize RSEs
```
./tools/run_tests_docker.sh -ir
```

8. Repeat the following steps
```
./bin/rucio-conveyor-preparer --run-once
./bin/rucio-conveyor-throttler --run-once
./bin/rucio-conveyor-submitter --run-once
./bin/rucio-conveyor-poller --run-once # Repeat ad nauseam (or until transfer is finished)
./bin/rucio-conveyor-finisher --run-once
```

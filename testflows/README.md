## Setup
Be sure to copy `5fca1cb1.0` and `5fca1cb1.signing_policy` from `../cluster/docker/` to this directory.
In addition, you will need to copy `ruciouser.pem` and `ruciouser.key.pem` from the Rucio certs.
If you are starting from scratch, you will need to make these yourself.
Otherwise, it should be as easy as running `make create` to deploy the `tpc-master` pod.

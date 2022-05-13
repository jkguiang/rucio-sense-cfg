# Networking Setup

XRootD binds to the interface defined in the `xrd.network` directive in the configuration. Under the constraint of limited physical NICs, spawning N instances of XRootD on the same host using different IPv6s, N virtual interfaces are required.

Given a physical interface `vlan.4070` (why is it also a VLAN? Don't ask...), an overlay virtual interface `vlan.4070-mac0` with IP `2001:48d0:3001:111::300` can be created using:
```
sudo ip link add link vlan.4070-mac0 link vlan.4070 type macvlan mode bridge
sudo ip -6 addr add 2001:48d0:3001:111::300/64 dev macvlan0
sudo ip link set up macvlan0
sudo ip -6 r add 2001:48d0:3001:111::300 dev macvlan0 table macvlan0
sudo ip -6 route add default via 2001:48d0:3001:111::1 dev macvlan0 table macvlan0
sudo ip -6 rule add from 2001:48d0:3001:111::300/128 table macvlan0
sudo ip -6 rule add to 2001:48d0:3001:111::300/128 table macvlan0
```
For creating another virtual interface, simply replace `mac0`, `macvlan0`, and the IPv6s in the commands above.

## Redirector-Specific Configuration
If one chooses to use IPv6s in the same `/64` subnet, an issue might arise where the default routing scheme is to use a single macvlan as the gateway for all N macvlans. However, this renders the setup unusable since all the origins subscribe to the redirectors using the same IP.

One solution is to manually change the routing tables such that each origin routes to the IP of its corresponding redirector. That is, in the origin host machine,

```
route -A inet6 add <REDIRECTOR_IP>/128 dev macvlan1
```

## Configured VLANs on `nrp-dev`
```
16 /64's , active with the ::1 address on the SN3700:
2001:48d0:fff:990::2/127, Vlan990
2001:48d0:3001:110::/64, Vlan4070
2001:48d0:3001:111::/64, Vlan4071
2001:48d0:3001:112::/64, Vlan4072
2001:48d0:3001:113::/64, Vlan4073
2001:48d0:3001:114::/64, Vlan4074
2001:48d0:3001:115::/64, Vlan4075
2001:48d0:3001:116::/64, Vlan4076
2001:48d0:3001:117::/64, Vlan4077
2001:48d0:3001:118::/64, Vlan4078
2001:48d0:3001:119::/64, Vlan4079
2001:48d0:3001:11a::/64, Vlan4080
2001:48d0:3001:11b::/64, Vlan4081
2001:48d0:3001:11c::/64, Vlan4082
2001:48d0:3001:11d::/64, Vlan4083
2001:48d0:3001:11e::/64, Vlan4084
2001:48d0:3001:11f::/64, Vlan4085
```

# Cluster Deployment

Kubernetes deployment yamls for the Rucio-SENSE XRootD cluster are automatically created by the `mkdeploy.py` script in the redi (redirector) and server (origin) directories.
Before running these scripts, you must first modify the environment variable `RUCIO_KEY_PASSWORD` in `certs/generate.sh`:
```
export RUCIO_KEY_PASSWORD=123456 # replace 123456 with your password
```
You must have also generated the Rucio CA/certs [here](https://github.com/aaarora/rucio/tree/master/etc/certs) with that same password.
Finally, you must also copy the private key used to create the Rucio CA to `certs/rucio_ca.key.pem`.
Then, once you've edited your configs appropriately, you can create the Kubernetes deployment yamls and run `make deploy`.

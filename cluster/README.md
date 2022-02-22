# Networking Setup

XRootD binds to the interface defined in the `xrd.network` directive in the configuration. Under the constraint of limited physical NICs, spawning N instances of XRootD on the same host using different IPv6s, N virtual interfaces are required.

Given a physical interface `en02`, an overlay virtual interface `en02mac` with IP `2605:d9c0::4a` can be created using:

```
ip link add link en02mac0 link en02 type macvlan mode bridge
ip -6 addr add 2605:d9c0::4a/64 dev macvlan0
ip link set up macvlan0
```
## Redirector-Specific Configuration
If one chooses to use IPv6s in the same `/64` subnet, an issue might arise where the default routing scheme is to use a single macvlan as the gateway for all N macvlans. However, this renders the setup unusable since all the origins subscribe to the redirectors using the same IP.

One solution is to manually change the routing tables such that each origin routes to the IP of its corresponding redirector. That is, in the origin host machine,

```
route -A inet6 add <REDIRECTOR_IP>/128 dev macvlan1
```

#!/bin/sh

ip -6 route del default via fe80::ecee:eeff:feee:eeee
ip -6 route add default via 2001:48d0:3001:111::1 dev net1 metric 1024 pref medium

#!/bin/sh

yum -y install iproute

ip -6 route del default via fe80::ecee:eeff:feee:eeee

for i in {0..40}; do dd if=/dev/zero of=/rucio/testSourceFile$i bs=1G count=1; done

#!/bin/sh

ip -6 route del default via fe80::ecee:eeff:feee:eeee

mkdir -p /rucio/store/data/Run2018A/EGamma/MINIAOD/UL2018_MiniAODv2-v1/50000/
for i in $(seq 0 $1); do 
  dd if=/dev/zero of=/rucio/testSourceFile$i bs=1G count=1;
  ln /rucio/testSourceFile$i /rucio/store/data/Run2018A/EGamma/MINIAOD/UL2018_MiniAODv2-v1/50000/testSourceFile$i.root  
done

chown -R xrootd:xrootd /rucio/*

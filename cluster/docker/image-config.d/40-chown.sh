#!/bin/bash

chown xrootd:xrootd /etc/xrootd/auth-file
chown -R xrootd:xrootd /etc/xrootd/checksum

mkdir /rucio/cksums
chmod 777 /rucio/cksums

chmod +x /etc/xrootd/checksum/adler.py

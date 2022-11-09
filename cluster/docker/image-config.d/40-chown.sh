#!/bin/bash

chown xrootd:xrootd /etc/xrootd/auth-file
chown -R xrootd:xrootd /etc/xrootd/checksum

chmod +x /etc/xrootd/checksum/adler.py

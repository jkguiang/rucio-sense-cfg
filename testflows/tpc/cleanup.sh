#!/bin/bash

for i in $(seq 0 $1); 
do
  gfal-rm -E /home/tpc/usercert.pem --key /home/tpc/userkey.pem davs://sense-origin-01.ultralight.org:1094//store/temp/testDestFile$i;
done

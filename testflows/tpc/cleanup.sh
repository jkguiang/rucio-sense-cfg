#!/bin/bash

for fname in $(gfal-ls -E /home/tpc/usercert.pem --key /home/tpc/userkey.pem  https://sense-origin-01.ultralight.org:1094//store/temp/ | grep testDestFile); do 
  gfal-rm -E /home/tpc/usercert.pem --key /home/tpc/userkey.pem davs://sense-origin-01.ultralight.org:1094//store/temp/$fname
done

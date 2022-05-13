#!/bin/bash

for fname in $(gfal-ls https://sense-origin-01.ultralight.org:1094//store/temp/ | grep testDestFile); do 
  gfal-rm davs://sense-origin-01.ultralight.org:1094//store/temp/$fname
done

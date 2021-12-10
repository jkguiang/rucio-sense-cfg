#! /bin/bash

nvmes=($(nvme list | awk '{print $1}'))
for i in ${!nvmes[@]}; do
    if [ "$i" -gt "2" ]; then
        j=$(( i - 2 ))
        mkdir /nvme${j}
        mount -t xfs ${nvmes[$i]} /nvme${j}
    fi
done
chown xrootd:xrootd /nvme*
chown xrootd:xrootd /mnt

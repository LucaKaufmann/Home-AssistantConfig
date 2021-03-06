#!/bin/bash
filesize=$(wc -c < /images/vacuum_maps/latest.png)
filesizeSnapshot=$(wc -c < /images/vacuum_maps/snapshot1.png)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    cp /images/vacuum_maps/snapshot5.png /images/vacuum_maps/snapshot5_"$(date -r /images/vacuum_maps/snapshot5.png +"%Y%m%d_%H%M%S").png"
    mv /images/vacuum_maps/snapshot4.png /images/vacuum_maps/snapshot5.png
    mv /images/vacuum_maps/snapshot3.png /images/vacuum_maps/snapshot4.png
    mv /images/vacuum_maps/snapshot2.png /images/vacuum_maps/snapshot3.png
    mv /images/vacuum_maps/snapshot1.png /images/vacuum_maps/snapshot2.png
    cp /images/vacuum_maps/latest.png /images/vacuum_maps/snapshot1.png
fi

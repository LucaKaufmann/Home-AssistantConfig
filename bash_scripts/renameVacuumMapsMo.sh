#!/bin/bash
filesize=$(wc -c < /images/vacuum_maps_mo/latest.png)
filesizeSnapshot=$(wc -c < /images/vacuum_maps_mo/snapshot1.png)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    cp /images/vacuum_maps_mo/snapshot5.png /images/vacuum_maps_mo/snapshot5_"$(date -r /images/vacuum_maps_mo/snapshot5.png +"%Y%m%d_%H%M%S").png"
    mv /images/vacuum_maps_mo/snapshot4.png /images/vacuum_maps_mo/snapshot5.png
    mv /images/vacuum_maps_mo/snapshot3.png /images/vacuum_maps_mo/snapshot4.png
    mv /images/vacuum_maps_mo/snapshot2.png /images/vacuum_maps_mo/snapshot3.png
    mv /images/vacuum_maps_mo/snapshot1.png /images/vacuum_maps_mo/snapshot2.png
    cp /images/vacuum_maps_mo/latest.png /images/vacuum_maps_mo/snapshot1.png
fi

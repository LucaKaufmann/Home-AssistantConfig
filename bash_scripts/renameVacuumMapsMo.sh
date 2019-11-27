#!/bin/bash
filesize=$(wc -c < /images/vacuum_maps_mo/latest.jpg)
filesizeSnapshot=$(wc -c < /images/vacuum_maps_mo/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    cp /images/vacuum_maps_mo/snapshot5.jpg /images/vacuum_maps_mo/snapshot5_"$(date -r /images/vacuum_maps_mo/snapshot5.jpg +"%Y%m%d_%H%M%S").jpg"
    mv /images/vacuum_maps_mo/snapshot4.jpg /images/vacuum_maps_mo/snapshot5.jpg
    mv /images/vacuum_maps_mo/snapshot3.jpg /images/vacuum_maps_mo/snapshot4.jpg
    mv /images/vacuum_maps_mo/snapshot2.jpg /images/vacuum_maps_mo/snapshot3.jpg
    mv /images/vacuum_maps_mo/snapshot1.jpg /images/vacuum_maps_mo/snapshot2.jpg
    cp /images/vacuum_maps_mo/latest.jpg /images/vacuum_maps_mo/snapshot1.jpg
fi

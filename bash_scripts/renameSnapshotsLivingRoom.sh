#!/bin/bash
filesize=$(wc -c < /images/logi/latest.jpg)
filesizeSnapshot=$(wc -c < /images/logi/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    # cp /images/logi/snapshot5.jpg /videos/images/snapshot_"$(date -r /images/logi/snapshot5.jpg +"%Y%m%d_%H%M%S").jpg"
    mv /images/logi/snapshot4.jpg /images/logi/snapshot5.jpg
    mv /images/logi/snapshot3.jpg /images/logi/snapshot4.jpg
    mv /images/logi/snapshot2.jpg /images/logi/snapshot3.jpg
    mv /images/logi/snapshot1.jpg /images/logi/snapshot2.jpg
    cp /images/logi/latest.jpg /images/logi/snapshot1.jpg
fi

#!/bin/bash
filesize=$(wc -c < /images/raspberry/latest.jpg)
filesizeSnapshot=$(wc -c < /images/raspberry/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    mv /images/raspberry/snapshot4.jpg /images/raspberry/snapshot5.jpg
    mv /images/raspberry/snapshot3.jpg /images/raspberry/snapshot4.jpg
    mv /images/raspberry/snapshot2.jpg /images/raspberry/snapshot3.jpg
    mv /images/raspberry/snapshot1.jpg /images/raspberry/snapshot2.jpg
    cp /images/raspberry/latest.jpg /images/raspberry/snapshot1.jpg
fi

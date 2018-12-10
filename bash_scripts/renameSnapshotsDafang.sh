#!/bin/bash

filesize=$(wc -c < /images/dafang/latest.jpg)
filesizeSnapshot=$(wc -c < /images/dafang/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        echo "Same size"
        exit
    fi
    echo "renaming"
    mv /images/dafang/snapshot4.jpg /images/dafang/snapshot5.jpg
    mv /images/dafang/snapshot3.jpg /images/dafang/snapshot4.jpg
    mv /images/dafang/snapshot2.jpg /images/dafang/snapshot3.jpg
    mv /images/dafang/snapshot1.jpg /images/dafang/snapshot2.jpg
    cp /images/dafang/latest.jpg /images/dafang/snapshot1.jpg
fi


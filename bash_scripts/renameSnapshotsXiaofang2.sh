#!/bin/bash
filesize=$(wc -c < /images/xiaofang2/latest.jpg)
filesizeSnapshot=$(wc -c < /images/xiaofang2/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    mv /images/xiaofang2/snapshot4.jpg /images/xiaofang2/snapshot5.jpg
    mv /images/xiaofang2/snapshot3.jpg /images/xiaofang2/snapshot4.jpg
    mv /images/xiaofang2/snapshot2.jpg /images/xiaofang2/snapshot3.jpg
    mv /images/xiaofang2/snapshot1.jpg /images/xiaofang2/snapshot2.jpg
    cp /images/xiaofang2/latest.jpg /images/xiaofang2/snapshot1.jpg
fi

#!/bin/bash
filesize=$(wc -c < /images/xiaofang1/latest.jpg)
filesizeSnapshot=$(wc -c < /images/xiaofang1/snapshot1.jpg)
minimumsize=0
if [ $filesize -gt $minimumsize ]; then
    if [ $filesize -eq $filesizeSnapshot ]; then
        exit
    fi
    mv /images/xiaofang1/snapshot4.jpg /images/xiaofang1/snapshot5.jpg
    mv /images/xiaofang1/snapshot3.jpg /images/xiaofang1/snapshot4.jpg
    mv /images/xiaofang1/snapshot2.jpg /images/xiaofang1/snapshot3.jpg
    mv /images/xiaofang1/snapshot1.jpg /images/xiaofang1/snapshot2.jpg
    cp /images/xiaofang1/latest.jpg /images/xiaofang1/snapshot1.jpg
fi

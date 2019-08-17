#!/bin/bash

ffmpeg -rtsp_transport tcp -y -i "rtsp://192.168.92.60:8554/unicast" -vcodec copy -c:a aac -strict experimental -map 0 -t 30 "/videos/capture-latest.mp4" 
FILE="$(date -r /videos/capture-latest.mp4 +"%Y%m%d_%H%M%S").mp4"
echo $FILE
cp /videos/capture-latest.mp4 /videos/capture_$FILE
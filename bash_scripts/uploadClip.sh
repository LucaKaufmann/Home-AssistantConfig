#!/bin/bash
 
FILE="$(date -r /media/Media/images/backyard/capture-latest.mp4 +"%Y%m%d_%H%M%S").mp4"

curl -X POST https://content.dropboxapi.com/2/files/upload \
    --header "Authorization: Bearer IMRguDRrx4gAAAAAAADi2mBlS1QopS4BuSUntmMm3qfntKwyk-DX8TELW-iOtSqj" \
    --header "Dropbox-API-Arg: {\"path\": \"/Videos/Cameras/Dafang/capture_$FILE\",\"mode\": \"add\",\"autorename\": true,\"mute\": false,\"strict_conflict\": false}" \
    --header "Content-Type: application/octet-stream" \
    --data-binary @/videos/capture-latest.mp4

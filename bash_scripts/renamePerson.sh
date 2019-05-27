#!/bin/bash
cp /images/raspberry/latest.jpg /images/persons/person_"$(date -r /images/vacuum_maps/snapshot5.png +"%Y%m%d_%H%M%S").png"

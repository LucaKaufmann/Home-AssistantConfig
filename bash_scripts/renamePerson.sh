#!/bin/bash
cp /images/raspberry/latest.jpg /images/persons/person_"$(date -r /images/raspberry/latest.jpg +"%Y%m%d_%H%M%S").jpg"

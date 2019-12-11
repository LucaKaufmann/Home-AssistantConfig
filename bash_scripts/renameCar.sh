#!/bin/bash
cp /images/raspberry/latest.jpg /images/cars/car_"$(date -r /images/raspberry/latest.jpg +"%Y%m%d_%H%M%S").jpg"

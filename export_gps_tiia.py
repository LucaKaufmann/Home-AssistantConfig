import csv
from pathlib import Path
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--rssi", dest="latitude",
                  help="rssi", action="store", type="float")
parser.add_option("-o", "--signal", dest="longitude",
                  help="signal", action="store", type="float")
parser.add_option("-d", "--ap", dest="date",
                  help="ap mac", action="store", type="string")

(options, args) = parser.parse_args()
latitude = options.latitude
longitude = options.longitude
date = options.date

values = Path("/config/export/tiia_gps.csv")
if values.is_file():
    with open('/config/export/tiia_gps.csv', 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([latitude,longitude,date])
else:
    with open('/config/export/tiia_gps.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['latitude','longitude','date'])
        newFileWriter.writerow([latitude,longitude,date])
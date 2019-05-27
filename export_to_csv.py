import csv
from pathlib import Path
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--rssi", dest="rssi",
                  help="rssi", action="store", type="int")
parser.add_option("-s", "--signal", dest="signal",
                  help="signal", action="store", type="int")
parser.add_option("-a", "--ap", dest="ap",
                  help="ap mac", action="store", type="string")
parser.add_option("-l", "--location", dest="location",
                  help="location", action="store", type="string")

(options, args) = parser.parse_args()
rssi = options.rssi
signal = options.signal
ap = options.ap
location = options.location

values = Path("/config/export/wifi_values.csv")
if values.is_file():
    with open('/config/export/wifi_values.csv', 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([rssi,signal,ap,location])
else:
    with open('/config/export/wifi_values.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['rssi','signal','mac','location'])
        newFileWriter.writerow([rssi,signal,ap,location])
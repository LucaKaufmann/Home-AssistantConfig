import csv
from pathlib import Path
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--rssi", dest="rssi",
                  help="rssi", action="store", type="int")
parser.add_option("-s", "--signal", dest="signal",
                  help="signal", action="store", type="int")
parser.add_option("-a", "--ap", dest="ap",
                  help="ap mac", action="store", type="int")
parser.add_option("-d", "--downstairs", dest="downstairs",
                  help="downstairs", action="store", type="int")

(options, args) = parser.parse_args()
rssi = options.rssi
signal = options.signal
ap = options.ap
downstairs = options.downstairs

values = Path("/config/export/values.csv")
if values.is_file():
    with open('/config/export/values.csv', 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([rssi,signal,ap,downstairs])
else:
    with open('/config/export/values.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['rssi','signal','mac','downstairs'])
        newFileWriter.writerow([rssi,signal,ap,downstairs])
import csv
from pathlib import Path

rssi = data.get('rssi')
signal = data.get('signal')
ap = data.get('ap_mac')
downstairs = data.get('downstairs')

values = Path("/config/values.csv")
if values.is_file():
    with open('/config/values.csv', 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([rssi,signal,ap,downstairs])
else:
    with open('/config/values.csv','w') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['rssi','signal','mac','downstairs'])
        newFileWriter.writerow([rssi,signal,ap,downstairs])
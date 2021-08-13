import tkinter     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta
import json, re, csv

tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
if len(filename) < 1:
    exit()
print(filename)

cal_name = ''
cal_entries=[]
lines = []
others = []
pattern = '%Y%m%dT%H%M%SZ'

with open(filename, 'r') as a_file:
    for line in a_file:
        stripped_line = line.strip()
        #print(stripped_line)
        lines.append(stripped_line)

cal_name = str(lines[5]).replace('X-WR-CALNAME:', '')

for i in range(len(lines)):    
    if lines[i] == 'BEGIN:VEVENT':
        temp = {}
        i += 1
        while lines[i] != 'END:VEVENT':
            #print(lines[i])
            for token in lines[i].split(';'):
                t_line = re.split('[A-Z]:', token)
                result = re.search('[A-Z]:',token)
                if result is not None:
                    splitat = result.start() 
                    if len(t_line) >1 and splitat > 2:
                        key = str(token[:splitat+2]).replace(':','',1)
                        value = token[splitat+2:]
                        temp[key] = value
            i += 1
            
        dt = datetime.strptime(temp['CREATED'], pattern)
        temp['CREATED_UTC'] = temp['CREATED']
        temp['CREATED'] = str(dt + timedelta(hours=-7))
        
        if 'DTSTART' in temp:
            dt = datetime.strptime(temp['DTSTART'], pattern)
            temp['DTSTART_UTC'] = temp['DTSTART']
            temp['DTSTART'] = str(dt + timedelta(hours=-7))
        
            limited = {}
            limited['DTSTART'] = temp['DTSTART']
            limited['DTEND'] = temp['DTEND']
            limited['DTSTAMP'] = temp['DTSTAMP']
            limited['CREATED'] = temp['CREATED']
            limited['DESCRIPTION'] = temp['DESCRIPTION']
            limited['LAST-MODIFIED'] = temp['LAST-MODIFIED']
            limited['LOCATION'] = temp['LOCATION']
            limited['SEQUENCE'] = temp['SEQUENCE']
            limited['STATUS'] = temp['STATUS']
            limited['SUMMARY'] = temp['SUMMARY']
            limited['TRANSP'] = temp['TRANSP']
            limited['CREATED_UTC'] = temp['CREATED_UTC']
            limited['DTSTART_UTC'] = temp['DTSTART_UTC']
        
            cal_entries.append(limited)
        else:
            others.append(temp)
        
    temp = {}
    
#print(json.dumps(cal_entries, indent = 4))
data_file = open(filename.replace('.ics',".csv"), 'w', encoding='utf-8')
keys = cal_entries[0].keys()

csv_writer = csv.DictWriter(data_file, keys, lineterminator='\n')

csv_writer.writeheader()
csv_writer.writerows(cal_entries)
        
for entry in others:
    #csv_writer.writerow(entry)
    print(entry)

data_file.close()

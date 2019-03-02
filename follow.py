# follow.py
#
# Follow a file like tail -f.

'''import time

logfile = open(r'/Users/das/data2.0/data2_FileUploadUtility/log.txt',"r")
logfile.seek(0,0)
while True:
    line = logfile.readline()
    if not line:
            time.sleep(1)
            continue
    print(line)
'''

import os.path
import time
file_path=r'/Users/das/data2.0/data2_FileUploadUtility/log1.txt'
while not os.path.exists(file_path):
    time.sleep(1)

if os.path.isfile(file_path):
    logfile = open(file_path,"r")
    content = logfile.read()
    print(content)
else:
    pass
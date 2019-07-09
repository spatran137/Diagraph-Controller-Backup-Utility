#!C:\Program Files\Python36\python.exe

##################################################
## This is to backup the configuration and files
## on a Diagraph IJ3000 and IJ4000 case printer
##################################################
## GNU Lesser General Public License v3.0
##################################################
## Author: Patrick Hinson
## Copyright: Copyright 2018, Diagraph Backup Utility
## Credits: [Patrick Hinson]
## License: GNU Lesser General Public License v3.0
## Version: 1.0.0
## Mmaintainer: Patrick Hinson
## Email: 
## Status: Stable
##################################################

## This is simply to avoid from having to use windows
## task manager or any other OS scheduler.

import time
import os
import sys
import schedule
import Diagraph_Controller_Backup

schedule.every().day.at("17:00").do(Diagraph_Controller_Backup.start)
schedule.every().day.at("5:00").do(Diagraph_Controller_Backup.start)
print('Schedule backup is running will backup at 1700 and 0500 each day')
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except:
    print("Main() Unexpected error:", sys.exc_info()[0])

#!C:\Program Files\Python36\python.exe

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

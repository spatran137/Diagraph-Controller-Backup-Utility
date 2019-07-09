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

import urllib.request
import shutil
import time
import sys
import os
import subprocess
import csv

#makes sure that both the dir and file exists and if not this will create them
def mkdrfl(file):
    try:
        directory = os.path.dirname(file)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(file):
                open(file, 'w').close()
    except:
        exerror = "mkdrfl() Unexpected error:", sys.exc_info()[0]
        print(exerror)
#Backup proces
def backup(ip, devicename):
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")

    #constructs the URL for the backup
    url = 'http://' + ip + '/backup.cgi'

    #finds the current working dir and builds the UNC path for the file.
    #the backup folder will be located in the same directory as the python files.
    cwd = os.getcwd()
    file_path = "BackUp/" + year + "/" + month + "/" + day + "/"
    file_path = os.path.join(cwd, file_path)

    #verifies that the directory exists and if it does not then it creates it
    mkdrfl(file_path)

    #builds the file name
    ftime = time.strftime("%Y.%m.%d--%H.%M")
    filename = file_path + devicename + '--' + ip + '--' + ftime + '.tgz'

    #prints to screen the start of what currently being backed up.
    print(devicename + ' has started to backup. ' + ftime)

    # starts the download of the backup file from the controller.
    with urllib.request.urlopen(url) as download, open(filename, 'wb') as outfile:
        shutil.copyfileobj(download, outfile)

    #prints to screen when the backup is done
    dtime = time.strftime("%Y.%m.%d--%H.%M")
    print(devicename + ' is done with the backup. ' + dtime)

#pings the printer to make sure it is alive.
def ping(host):
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-n', '2', '-w', '700', host],
                stdout=DEVNULL, 
                stderr=DEVNULL
            )
            is_up = True
            up = 'Ping: Up ' + host
            return is_up
        except subprocess.CalledProcessError:
            is_up = False
            return is_up

def start():

    #adds the current working dir to the device csv
    cwd = os.getcwd()
    csvpath = os.path.join(cwd, "devices.csv")

    #reads the .csv and for each line stores it into two vars.
    #if the controller is alive the backup will start if not then it will just print to screen and move on.
    try:
       with open(csvpath, newline='') as f:
           reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
           for row in reader:

               ip = row[0]
               devicename = row[1]

               result = ping(ip)

               if result == True:
                   backup(ip, devicename)
               elif result == False:
                    print(ip + ' ' + devicename + ' not reachable')
    except:
       exerror = "Start() Unexpected error:", sys.exc_info()[1]
       print(exerror)

if __name__ == '__main__':
    try:
        start()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        exerror = "__main__ Unexpected error:", sys.exc_info()[0]
        print(exerror)

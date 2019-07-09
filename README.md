https://travis-ci.org/spatran137/Diagraph-Controller-Backup-Utility.svg?branch=master

# Diagraph-Controller-Backup
Backup utility to backup the controller’s configuration.  It does this via backup.cgi through the web interface.  This was written to backup twice a day.
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Limitations

This was not intended to do much other than automate the task of backing up the controllers configuration.  The backups themselves are stored in a folder structure located in the same directory as the python files.

### Prerequisites

Here are the packages that will need to be installed/used in this project:

```
requests==2.20.0
schedule==0.4.3
```
```
pip install -r (the path to where requirements.txt is located)
```
### Installing

Once downloaded add the controllers to the devices.csv file IP Address, then the Printer name:

```
192.168.0.1,printer1
192.168.0.2,printer2
```

The name will not affect the execution it is there to be human friendly.

## Schedule

As is the backup-schedule.py will run the backups twice a day at 500 and 1700 every day.  To change this, edit the backup-schedule.py:

Lines 9 and 10 and change the times.
```
schedule.every().day.at("17:00").do(Diagraph_Controller_Backup.start)
schedule.every().day.at("5:00").do(Diagraph_Controller_Backup.start)
```


## Built With

* [requests](https://pypi.python.org/pypi/requests) - Used to download the files
* [schedule](https://github.com/dbader/schedule) - Used to schedule when the backups run

## Authors

* **Patrick Hinson** - *Initial work* - [spatran137](https://github.com/spatran137)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

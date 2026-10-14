# Diagraph Controller Backup Utility

> [!WARNING]
> **Legacy / unmaintained repository:** This project is preserved for historical and reference use only. It is not receiving further updates, bug fixes, security fixes, compatibility work, or support. Use it at your own risk and fork it if you need to make changes.

This Windows-oriented Python utility downloads configuration backups from Diagraph IJ3000 and IJ4000 case-printer controllers. For each configured controller, it checks ICMP reachability and then downloads the response from:

```text
http://<controller>/backup.cgi
```

The response is saved as a dated `.tgz` file. The utility can run once on demand or remain in the foreground and start backups at two configured times each day.

## How it works

For each row in `devices.csv`, the utility:

1. Runs the Windows `ping` command against the controller.
2. Skips the controller if the ping fails.
3. Sends an unauthenticated HTTP request to `/backup.cgi` if the ping succeeds.
4. Saves the response under a date-based directory in the current working directory.

Controllers are processed sequentially.

## Requirements

- Windows. The reachability check uses the Windows-specific `ping -n 2 -w 700` syntax.
- Python 3. The scripts were written in the Python 3.6 era and are not tested against current Python releases.
- Network access to each controller over ICMP and HTTP.
- A controller firmware version that exposes `http://<controller>/backup.cgi` without authentication.
- Write access to the directory from which the script is launched.

The one-time backup script uses only the Python standard library. Scheduled mode also imports the third-party `schedule` package.

`requirements.txt` preserves the original dependency pins:

```text
requests==2.20.0
schedule==0.4.3
```

`requests` is not used by the current code; downloads use `urllib.request`. Both pins are historical and may have compatibility or security issues. If you reproduce the original environment, use an isolated virtual environment and assess the dependencies before using them on a production system.

## Setup

Clone the repository and change into it:

```powershell
git clone https://github.com/spatran137/Diagraph-Controller-Backup-Utility.git
cd Diagraph-Controller-Backup-Utility
```

For scheduled mode, create an isolated environment and install the legacy requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The shebangs in the scripts point to `C:\Program Files\Python36\python.exe`, but explicitly invoking the scripts with `python` avoids relying on that historical path.

## Configure controllers

Edit `devices.csv`. It is a headerless CSV file whose first two fields are:

```text
controller-address,friendly-name
```

Example:

```csv
192.168.0.10,Line-1
printer-02.example.local,Line-2
```

Configuration rules:

- Do not add a header row, comments, or blank lines.
- Every row must contain an address and a friendly name.
- Only the first two comma-separated fields are used.
- Whitespace is not trimmed.
- Use names that are safe in Windows filenames. The friendly name and controller address are inserted into the backup filename without sanitization.
- Treat a real device inventory as potentially sensitive; avoid publishing it unintentionally.

## Run one backup cycle

Run the command from the repository directory so the script can find `devices.csv` and place output where expected:

```powershell
python Diagraph_Controller_Backup.py
```

A reachable controller produces messages similar to:

```text
Line-1 has started to backup. 2026.10.14--17.00
Line-1 is done with the backup. 2026.10.14--17.00
```

An unsuccessful ping prints:

```text
192.168.0.10 Line-1 not reachable
```

## Backup output

Backups are written beneath `BackUp` in the **current working directory**, not necessarily beside the Python files:

```text
BackUp/
└── YYYY/
    └── MM/
        └── DD/
            └── <friendly-name>--<controller>--YYYY.MM.DD--HH.MM.tgz
```

For example:

```text
BackUp/2026/10/14/Line-1--192.168.0.10--2026.10.14--17.00.tgz
```

The `.tgz` extension reflects the expected response from the controller. The utility does not verify that the downloaded data is a valid archive.

## Run on the built-in schedule

Start the foreground scheduler from the repository directory:

```powershell
python backup-schedule.py
```

As shipped, it schedules a backup cycle every day at 05:00 and 17:00 according to the computer's local clock:

```python
schedule.every().day.at("17:00").do(Diagraph_Controller_Backup.start)
schedule.every().day.at("5:00").do(Diagraph_Controller_Backup.start)
```

Edit those two calls in `backup-schedule.py` to change the times.

The scheduler:

- must remain running in the foreground;
- does not install itself as a Windows service or scheduled task;
- does not run a backup immediately at startup;
- does not backfill a run missed while the process was stopped; and
- checks for pending jobs once per second.

For unattended use, an operating-system scheduler or supervised service is generally more reliable than this legacy foreground loop.

## Security and operational limitations

This software is intentionally small and has significant limitations:

- Controller traffic uses plain HTTP with no TLS, authentication, or certificate validation. Use it only on a trusted management network and only with controllers you are authorized to access.
- ICMP ping is a mandatory gate. A controller that blocks ping is skipped even if `/backup.cgi` is available.
- HTTP downloads have no explicit timeout, retry, integrity check, content validation, or atomic temporary-file handling.
- An interrupted or failed download can leave a partial `.tgz` file.
- A malformed CSV row or a download error can stop the remaining devices in that backup cycle.
- Broad exception handling prints an error but may still leave the process with a successful exit status.
- Devices are backed up one at a time.
- Filenames have one-minute precision. Repeating a backup for the same device within the same minute can overwrite the earlier file.
- There is no retention policy, pruning, compression management, encryption at rest, disk-space check, structured logging, notification, or monitoring.
- Backup archives may contain sensitive controller configuration. Protect the output directory and monitor its storage use.
- There are no automated tests. The historical Travis configuration is not evidence that controller backups still work.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `<address> <name> not reachable` | Confirm the address, network route, and Windows firewall rules. The controller must answer ICMP ping. |
| No backup runs immediately after starting `backup-schedule.py` | The scheduler waits until the next configured time. Run `Diagraph_Controller_Backup.py` for an immediate cycle. |
| `devices.csv` cannot be found | Launch the script from the repository directory. Paths are resolved from the current working directory. |
| An index or CSV-related error appears | Remove headers, blank lines, comments, and rows that do not contain at least an address and a name. |
| A request fails or hangs | Confirm that `http://<controller>/backup.cgi` is reachable for that controller and firmware. The code has no explicit HTTP timeout or retry. |
| Output appears in an unexpected location | Check the directory from which Python was launched; `BackUp` is created there. |
| A file cannot be created | Confirm write permissions and use filename-safe values in `devices.csv`. |

## Repository contents

| Path | Purpose |
| --- | --- |
| `Diagraph_Controller_Backup.py` | Reads the device list, checks reachability, downloads backups, and writes the dated files. |
| `backup-schedule.py` | Runs the backup function at the configured daily times. |
| `devices.csv` | Headerless controller inventory in `address,name` format. |
| `requirements.txt` | Historical dependency pins used by the scheduler environment. |
| `.travis.yml` | Historical CI configuration; it does not contain an automated test suite. |
| `LICENSE` | GNU Lesser General Public License version 3. |

## Author

Originally created by [Patrick Hinson](https://github.com/spatran137).

## License

Licensed under the [GNU Lesser General Public License v3.0](LICENSE).

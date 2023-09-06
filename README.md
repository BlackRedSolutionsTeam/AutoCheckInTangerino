# Auto check-in for Tangerino
 Project just for study purpose in python


## Libs to install in Ubuntu:

```
$ sudo apt-get install python3 chromium-chromedriver && pip install workalendar && pip install -U selenium
```

## Crontab: 

```
crontab -e
```

if u start at 09:00 AM
and finish work at 06:00 PM
I recommend: 
```
0 9 * * * cd /home/USER/AutoCheckInTangerino && python3 program.py
57 17 * * * cd /home/USER/AutoCheckInTangerino && python3 program.py
```






Remove winsound lib if not using windows.


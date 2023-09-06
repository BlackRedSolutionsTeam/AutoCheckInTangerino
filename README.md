# Auto check-in for Tangerino
 Project just for study purpose in python


Libs to install in Ubuntu:

```
$ apt-get install python3
```
```
$ pip install workalendar
```
```
$ pip install -U selenium
```
```
$ apt-get install chromium-chromedriver
```



Crontab:

in terminal linux:
```
crontab -e
```

if u start at 09:00 AM
and finish work at 06:00 PM
I recommend: 
```
0 9 * * * cd /home/vagnerking/AutoCheckInTangerino && python3 program.py
57 17 * * * cd /home/vagnerking/AutoCheckInTangerino && python3 program.py
```






Remove winsound lib if not using windows.


# meeting time controller

## Stakeholders
* presenters
* meeting organizer
* meeting coordinator

## Driver, Goal
* controlling agenda of the presentation
* keep on time track during the meeting
* controlling time of separate parts of the presentation
* detecting of the "hot presentation parts"

## Start of the console application
* with default file 'agenda.csv' in the same folder
```sh
python3 time-controller.py
```

* with specific agenda file 
```sh
python3 time-controller.py /home/temp/my-agenda.csv
```

* with specific agenda file and additional amount of minutes as a "spare time"
```sh
python3 time-controller.py /home/temp/my-agenda.csv 3
```

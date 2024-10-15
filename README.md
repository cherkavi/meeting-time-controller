# meeting time controller

## Stakeholders
* presenters
* meeting organizer
* meeting coordinator

## Drivers, Goals
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
python3 time-controller.py agenda.csv
```

* with specific agenda file and full amount of minutes for the session
```sh
python3 time-controller.py agenda.csv 10
```

* with specific agenda file and upcoming finish time 
```sh
python3 time-controller.py 22:40
```


## Application
### Modes
there are two possible modes of the working application:
1. Spare mode - when you are out of agenda (application starts in this mode)
2. ToDo mode - you are working on one of the agenda points

### Shortcuts
* **q** - quit
* **s** - Spare mode
* **t** - ToDo mode
* **n** - move to next Agenda point
* **p** - move to previous Agenda point 

### Input
* csv file where each line has name of the point and amount of minutes for it in your agenda  
  just specify the name of the file in any position as an input argument 
* int number in any position of an input argument as an initial amount of Spare minutes
* upcoming time in format "11:00" or "13:30" or "17:10" in any position 

### Output
after quit from the application  
you will find the snapshot of the last screen  
in "out_yyyyMMddHHmmss.txt" file 

### Screenshot
current mode - ToDo
1. finished point
2. currently active part of the meeting
3. upcoming chapter
4. current spare time is negative - need to speed up to catch the deadline (7)
5. start time
6. current time
7. end time
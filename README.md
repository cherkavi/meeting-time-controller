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
python3 time-controller.py /home/temp/my-agenda.csv
```

* with specific agenda file and additional amount of minutes as a "spare time"
```sh
python3 time-controller.py /home/temp/my-agenda.csv 3
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

### Output
after quit from the application  
you will find the snapshot of the last screen  
in "out_yyyyMMddHHmmss.txt" file 
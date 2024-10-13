import curses
import os
import csv
import time
from typing import List
import sys
import datetime

DEFAULT_FILE:str = 'agenda.csv'
LENGTH_NUMBER:int = 2
LENGTH_NUMBER_SPACE:int = 3
LENGTH_NAME:int=40
LENGTH_NAME_SPACE:int=5
LENGTH_TIME:int=10
LENGTH_TIME_SPACE:int=4
LENGTH_TIMEEND:int=10

def init_curses():
    screen = curses.initscr()    
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)    
    return screen

def terminate_curses(screen, return_screen_content:bool = False) -> str:
    screen_content = ""
    if return_screen_content:
        for each_line in range(0, curses.LINES):
            screen_content = screen_content + "\n" + screen.instr(each_line, 0, curses.COLS).decode('utf-8')        
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    return screen_content

screen = init_curses()

def color_num(byte_value:int) -> int:
    return int(byte_value/255*1000)

curses.start_color()
## Define colors
COLOR_BACKGROUND = 1  # WARNING, BUG !!!! all colors and pairs should be activated with increment 1!!! 
curses.init_color(COLOR_BACKGROUND, color_num(0), color_num(0), color_num(60))  
COLOR_INACTIVE = 2
curses.init_color(COLOR_INACTIVE, color_num(77), color_num(88), color_num(99)) 
COLOR_ACTIVE_SPARE = 3
curses.init_color(COLOR_ACTIVE_SPARE, color_num(0), color_num(0), color_num(200)) 
COLOR_ACTIVE_TODO = 4
curses.init_color(COLOR_ACTIVE_TODO, color_num(0), color_num(120), color_num(0)) 
COLOR_WARNING = 5
curses.init_color(COLOR_WARNING, color_num(120), color_num(0), color_num(0)) 

## Define color pairs
COLORPAIR_BACKGROUND = 1
curses.init_pair(COLORPAIR_BACKGROUND, COLOR_INACTIVE, COLOR_BACKGROUND)
screen.bkgd(' ', curses.color_pair(COLORPAIR_BACKGROUND))

COLORPAIR_INACTIVE = 2
curses.init_pair(COLORPAIR_INACTIVE, COLOR_INACTIVE, COLOR_BACKGROUND)

COLORPAIR_ACTIVE_SPARE = 3
curses.init_pair(COLORPAIR_ACTIVE_SPARE, COLOR_ACTIVE_SPARE, COLOR_BACKGROUND)

COLORPAIR_ACTIVE_TODO = 4
curses.init_pair(COLORPAIR_ACTIVE_TODO, COLOR_ACTIVE_TODO, COLOR_BACKGROUND)

COLORPAIR_WARNING = 5
curses.init_pair(COLORPAIR_WARNING, COLOR_WARNING, COLOR_BACKGROUND)

screen.refresh()

class AgendaItem:
    def __init__(self, name:str, duration:int):
        self.name = name
        self.duration = duration
        self.elapsed = 0

    def tik(self, seconds:int=1) -> int:
        self.elapsed += seconds
        self.duration -= seconds
        return self.duration
    
    def drain(self) -> int:
        self.elapsed = self.elapsed + self.duration
        return_value = self.duration
        self.duration = 0 
        return return_value

    def __str__(self):
        return f'{self.name} {self.duration} {self.elapsed}'

    def __repr__(self):
        return f'{self.name} {self.duration} {self.elapsed}'

    def __len__(self):
        return self.duration

def read_agenda_from_file(file_path: str) -> List[AgendaItem]:
    agenda: List[AgendaItem] = [] 
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            name, duration = row
            agenda.append(AgendaItem(name, int(duration)*60))
    return agenda


def read_agenda(file_paths: List[str]) -> List[AgendaItem]:
    # Use provided file paths if any, otherwise use default file
    files_to_check: List[str] = file_paths if file_paths else [DEFAULT_FILE]

    for file_path in files_to_check:
        if os.path.isfile(file_path):
            return read_agenda_from_file(file_path)
    
    sys.exit(f'No agenda file found in {files_to_check}')

def read_time(arguments: List[str]) -> int:
    for each_argument in arguments:
        if each_argument.isnumeric():
            return int(each_argument)*60
    return 0

def sec_to_time(value: int) -> str:
    seconds = abs(value)
    if seconds < 3600:
        if value < 0:
            return "  -"+str(datetime.timedelta(seconds=seconds))[2:]
        else:
            return "   "+str(datetime.timedelta(seconds=seconds))[2:]
    else:  
        if value < 0:
            return "-"+str(datetime.timedelta(seconds=seconds))
        else:
            return " "+str(datetime.timedelta(seconds=seconds))

def sec_to_fulltime(sec: int) -> str:
    return str(datetime.timedelta(seconds=sec))


def get_current_time_in_seconds():
    return datetime.datetime.now().hour*3600 + datetime.datetime.now().minute*60 + datetime.datetime.now().second


def print_agenda_line(screen, index: int, name_length:int, name: str, duration: int, mode_todo:bool, todo_index:int):
    row = index    
    if mode_todo and index == todo_index:
        if duration > 0:
            color = curses.color_pair(COLORPAIR_ACTIVE_TODO) | curses.A_BOLD | curses.A_REVERSE
        else:
            color = curses.color_pair(COLORPAIR_ACTIVE_SPARE) | curses.A_BOLD | curses.A_REVERSE
    else:
        color = curses.color_pair(COLORPAIR_INACTIVE)
    if duration == 0:
        color = color | curses.A_DIM
    screen.addstr(row, 0, 
                  f'{str(index+1).rjust(LENGTH_NUMBER)}', 
                  color)
    screen.addstr(row, LENGTH_NUMBER, " "*LENGTH_NUMBER_SPACE)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE, 
                  f'{name[:name_length].rjust(name_length)}', color)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length, 
                  " "*LENGTH_NAME_SPACE)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length+LENGTH_NAME_SPACE, 
                  f'{sec_to_time(duration).ljust(LENGTH_TIME)}', color)

def print_spare_time(screen, index: int, name_length:int, spare_time: int, mode_spare:bool, enough_time:bool):
    name = "Spare time"
    row = index
    if mode_spare:
        if enough_time:
            color = curses.color_pair(COLORPAIR_ACTIVE_SPARE) | curses.A_BOLD | curses.A_REVERSE
        else:
            color = curses.color_pair(COLORPAIR_WARNING) | curses.A_BOLD | curses.A_REVERSE
    else: 
        if enough_time:
            color = curses.color_pair(COLORPAIR_INACTIVE) 
        else:
            color = curses.color_pair(COLORPAIR_WARNING) | curses.A_BOLD | curses.A_REVERSE

    # check if not enough time

    screen.addstr(row, 0, 
                  " "*LENGTH_NUMBER)
    screen.addstr(row, LENGTH_NUMBER, 
                  " "*LENGTH_NUMBER_SPACE)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE, 
                  f'{name[:name_length].rjust(name_length)}', color)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length, 
                  " "*LENGTH_NAME_SPACE)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length+LENGTH_NAME_SPACE, 
                  f'{sec_to_time(spare_time).ljust(LENGTH_TIME)}', color)

def print_current_time(screen, index: int, name_length:int, start_time_in_sec: int, passed_seconds: int, end_time_in_sec:int, color_pair:int):
    row = index
    screen.addstr(row, 0, 
                  " "*LENGTH_NUMBER, 
                  curses.color_pair(color_pair))
    screen.addstr(row, LENGTH_NUMBER, 
                  " "*LENGTH_NUMBER_SPACE)
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE, 
                  f'{ sec_to_fulltime(start_time_in_sec).rjust(name_length)}', 
                  curses.color_pair(color_pair))
    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length, 
                  " "*LENGTH_NAME_SPACE)
    
    # !!! start_time_in_sec+passed_second == current time
    current_time = get_current_time_in_seconds()
    if current_time < start_time_in_sec + passed_seconds:
        time.sleep(0.1)

    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length+LENGTH_NAME_SPACE, 
                  f'{sec_to_fulltime(current_time).ljust(LENGTH_TIME)}', 
                  curses.color_pair(color_pair))

    screen.addstr(row, LENGTH_NUMBER+LENGTH_NUMBER_SPACE+name_length+LENGTH_NAME_SPACE+LENGTH_TIME+LENGTH_TIME_SPACE, 
                  f'{sec_to_fulltime(end_time_in_sec).ljust(LENGTH_TIMEEND)}', 
                  curses.color_pair(color_pair))
    

def draw_agenda(agenda: List[AgendaItem], full_time_sec: int) -> None:
    try:
        start_time_in_sec:int = get_current_time_in_seconds()
        spare_time:int = full_time_sec - sum([each_agenda.duration for each_agenda in agenda]) if full_time_sec > 0 else 0
        end_time_in_sec:int = get_current_time_in_seconds() + spare_time + sum([each_agenda.duration for each_agenda in agenda])
        current_sec:int = 0
        max_name_length:int = min(max([len(each_agenda.name) for each_agenda in agenda]) , LENGTH_NAME)

        screen.nodelay(True)        
        semi_seconds = False
        mode_spare:bool = True
        mode_todo:bool = False
        todo_index:int = 0

        while True:                        
            typed_char = screen.getch()
            if typed_char == ord('q'):
                break
            
            if typed_char == ord('s'):
                mode_spare = True
                mode_todo = False

            if typed_char == ord('t'):
                if todo_index < len(agenda):
                    mode_spare = False
                    mode_todo = True
                else:
                    # when all agenda items are done, do nothing
                    pass

            if typed_char == ord('p'):  
                if mode_todo:
                    if todo_index > 0:
                        todo_index -= 1

            if typed_char == ord('n'):  
                # next agenda
                if mode_todo:                    
                    if todo_index < len(agenda):
                        spare_time += agenda[todo_index].drain()
                        todo_index += 1                    
                    if todo_index == len(agenda):
                        mode_spare = True
                        mode_todo = False
                else:
                    mode_spare = False
                    mode_todo = True

            time.sleep(0.5)

            for index, item in enumerate(agenda):            
                print_agenda_line(screen, index, max_name_length, item.name, item.duration, mode_todo, todo_index)
            sum_duration = sum([abs(each_agenda.duration) for each_agenda in agenda])
            print_spare_time(screen, index+2, max_name_length, spare_time, mode_spare, start_time_in_sec+current_sec+sum_duration<end_time_in_sec)
            print_current_time(screen, index+3, max_name_length, start_time_in_sec, current_sec, end_time_in_sec, COLORPAIR_INACTIVE)
            
            if semi_seconds:
                semi_seconds = False
                current_sec += 1
                if mode_todo:
                    agenda[todo_index].tik()    
                if mode_spare:
                    spare_time -= 1
            else:
                semi_seconds = True

    except BaseException as e:
        print(f"exception: {e}")
    finally:
        terminate_curses(screen, True)


def main(arguments: List[str]) -> None:
    agenda:List[AgendaItem] = read_agenda(arguments)
    full_time_sec = read_time(arguments)
    draw_agenda(agenda, full_time_sec)

    
if __name__=='__main__':    
    arguments = sys.argv[1:] if len(sys.argv) > 1 else []
    main(arguments)

    # screen.refresh()
    curses.endwin()

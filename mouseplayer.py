"""logged mouse motion replay module

Example:
    In this case, mouse logged file is stored 'data/log01.csv'.  
    Log file made by "mouse_click_logger.py".

    mp = MousePlayer()
    mp.load_log("data/log01.csv")
    mp.replay()


"""
import csv
import time
import pprint
import pyautogui as pg
import pywinctl as wcl
from mousedata import MouseData

class MousePlayer:
    """class for replaying that logged mouse motion 
    """
    def __init__(self):
        self.input_data = []

    def load_log(self,logfile:str):
        """log file loading method
        TODO:other log file extensions
        """
        self.input_data = []
        with open(logfile, 'r',newline='',encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)       #skip header
            for row in reader:
                if(float(row[0])<0 or float(row[0])>1):     #change window
                    # raise ValueError("x out of range (0~1)")
                    continue
                if(float(row[1])<0 or float(row[1])>1):     #change window
                    # raise ValueError("y out of range (0~1)")
                    continue
                tmp = MouseData(x_in_window=float(row[0]),y_in_window=float(row[1]),time_interval=float(row[2]),title=row[3])
                self.input_data.append(tmp)

    def replay(self):
        """replay that logged mouse motion
        """
        # Make sure the window you wish to operate on is active.
        titles = wcl.getAllTitles()
        for data in self.input_data:
            if data.title not in titles:
                print("no active window you recorded, please launch the window")
                exit(1)

        #start replay
        for data in self.input_data:
            target_win = wcl.getWindowsWithTitle(data.title)[0]

            # Activate the window to operate
            active_win = wcl.getActiveWindowTitle()
            if active_win != data.title:
                target_win.activate()

            time.sleep(data.time_interval)
            self.click_xy_in_window(data,target_win)

    def click_xy_in_window(self,data:MouseData,hwnd,dur:float=0.2):
        """click xy in target window

        Args:
            data (MouseData): logged mouse motion data
            hwnd (Win32Window): target window handler
            dur (float): mouse click duration[sec]
        """
        x = int(hwnd.width * data.x_in_window) + hwnd.left
        y = int(hwnd.height * data.y_in_window) + hwnd.top
        pg.click(x,y,duration=dur)



def main():
    """main sequence (example)
    """
    mp = MousePlayer()
    mp.load_log("data/log01.csv")
    pprint.pprint(mp.input_data)
    mp.replay()

if __name__ == "__main__":
    main()
    
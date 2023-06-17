"""mouse click logger module
"""
import csv
import time
import pprint
import sys
import os
import mouse
import pyautogui as pg
from mousedata import MouseData

class MouseLogger():
    """class for logging mouse click
    """
    def __init__(self,outfile:str=None):
        self.time_interval:float = None
        self.active_window = pg.getActiveWindow()
        self.x_in_window = None
        self.y_in_window = None
        self.timestamp = time.time()
        self.log = []
        self.outfile = outfile
        self.out_mode = self.set_out_mode()
        # watch click event
        mouse.on_click(self.on_click_callback)

    def on_click_callback(self):
        """fuction to call when left click detected
        """
        print("left click detected!")
        self.get_xy_in_window()
        print(f"X:{self.x_in_window:.4f},  Y:{self.y_in_window:.4f},  title:{self.active_window.title}")
        tmp_time = time.time()
        tmp_mouse = MouseData(self.x_in_window,self.y_in_window,tmp_time-self.timestamp,self.active_window.title)
        self.timestamp = tmp_time
        self.log.append(tmp_mouse)

    def set_out_mode(self):
        """select saving mode from received output file extension
        TODO: add other file format
        """
        if(self.outfile is None):
            return "nothing"
        elif( self.outfile.endswith(".csv")):
            return "csv"
        else:
            print("The specified extension is not supported")
            return "nothing"
        
    def get_xy_in_window(self):
        """calculate xy coordinate (0~1) in active window
        """
        x, y = pg.position()
        if(x < self.active_window.left or
            x > self.active_window.left + self.active_window.width or
            y < self.active_window.top or
            y > self.active_window.top + self.active_window.height):
            print("out of range")
            time.sleep(0.8)
        self.active_window = pg.getActiveWindow()
        self.x_in_window = (x-self.active_window.left)/self.active_window.width
        self.y_in_window = (y-self.active_window.top)/self.active_window.height

    def output_log(self):
        """export mouse click log 

        Raises:
            ValueError: no applicable mode
        """
        if(self.out_mode == "nothing"):
            pass
        elif(self.out_mode == "csv"):
            self.outcsv()
        else:
            raise ValueError("No applicable mode")

    def outcsv(self):
        with open(self.outfile, 'w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y", "time_interval","window_title"])
            for tmplog in self.log:
                writer.writerow([tmplog.x_in_window, tmplog.y_in_window, tmplog.time_interval,tmplog.title])

def main():
    """main sequence
    """
    print('Press Ctrl-C to quit.')

    args = sys.argv
    if 2 != len(args):
        print("invalid command line args. please specify a input file.")
        exit()
    out_dir,out_path=os.path.split(args[1])
    if out_dir != '':
        print("please don't use relative path.")
        exit()

    mlog = MouseLogger(outfile=os.path.join("data",out_path))
    try:
        while True:
            time.sleep(1.5)
            print("waiting...")
    except KeyboardInterrupt:
        pprint.pprint(mlog.log)
        mlog.output_log()
        print('\n')

if __name__ == "__main__":
    main()
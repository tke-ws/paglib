#! python3
import pyautogui as pg 
import time
print('Press Ctrl-C to quit.')
try:
    activewin = pg.getActiveWindow()
    while True:
        x, y = pg.position()
        if(x < activewin.left or
            x > activewin.left + activewin.width or
            y < activewin.top or
            y > activewin.top + activewin.height):
            print("out of range           ",end='')
            print('\b' * len("out of range           "), end='',flush=True)
            time.sleep(0.4)
            activewin = pg.getActiveWindow()
            continue
        activewin = pg.getActiveWindow()
        positionStr = 'X: ' + str(f"{(x-activewin.left)/activewin.width:.4f}").rjust(6) + \
                     ' Y: ' + str(f"{(y-activewin.top)/activewin.height:.4f}").rjust(6)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='',flush=True)
except KeyboardInterrupt:
    print('\n')
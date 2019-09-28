import win32api,win32con,win32gui
import numpy as np
from time import sleep
a=win32api.GetCursorPos()
print(a)
def seta(loc):
    # sleep(1)
    win32api.SetCursorPos(loc)

def exe():
    b = np.array(a)-(200,200)
    print(b)
    seta(b)

def square():
    win32api.SetCursorPos((100,100))
    sleep(1)
    win32api.SetCursorPos((100,800))
    sleep(1)
    win32api.SetCursorPos((1643,800))
    sleep(1)
    win32api.SetCursorPos((1643,100))
    sleep(1)
    win32api.SetCursorPos((100,100))
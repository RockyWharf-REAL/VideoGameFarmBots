import time

import keyboard
import pydirectinput
import pynput

"""
Tool to help me get positions of things that I click on.
"""

positions = []
last_input = False
while not keyboard.is_pressed('q'):
    if keyboard.is_pressed('space'):
        if not last_input:
            print("CLICKED")
            last_input = True
            positions.append(pydirectinput.position())
    else:
        last_input = False

with open("positions.txt", "w") as f:
    for p in positions:
        f.write(str(p) + "\n")

import random
import sys
import threading
import time

import keyboard
import pyautogui
import pydirectinput
from yaml.scanner import Scanner

"""
Creator: RockyWharf
Version: 1.0

This script allows the user to input the max number of jumps there character can currently do.
The player will then jump as many times as possible, then glide.
    Quick note: the glide formula is for every 1 jump = 3 seconds of glide. 
    While terrain may cause this to vary, the glide will be jumps * 3 - (jumps/3).
        I am assuming you can at least jump more then 3... Right?
While in glide state, the player will attack with left and right click.
When time runs out, the player will fall back to the ground, being given (jumps/3) seconds.
Once they player (hopefully) has hit the ground, the player will start jumping into the air again and glide.
After 10-15 minutes, the player will auto join a new world starting the cycle over.
The x key is used to call your minecart, reseting our dragon/mount state.
We press z before starting to jump into the air
"""

"""
Valid worlds up to dragonfire peaks
(1099, 567)
(1038, 736)
(876, 763)
(854, 634)
(732, 681)
(725, 542)
(782, 365)
(992, 312)
(1230, 371)
"""
def world_reload():
    #This will be a list of valid mouse positions you can click onto.
    valid_world_selections = [[1099, 567],[1038, 736],[876, 763],[854, 634],[732, 681],[725, 542],[782, 365],[992, 312],[1230, 371]]
    world_index = random.randint(0, len(valid_world_selections) - 1)
    world_selected = valid_world_selections[world_index]

    # Open map menu
    pydirectinput.keyDown('ctrl')
    pydirectinput.keyDown('a')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('a')
    #Time for map to load
    time.sleep(1)

    pyautogui.click(world_selected[0] , world_selected[1])
    # Enter location (1732, 664)
    #Time enter to load
    time.sleep(1)
    # Let's just triple check we pressed that enter button :)
    pydirectinput.click(1732,664)
    time.sleep(0.1)
    pydirectinput.click(1732, 664)
    time.sleep(0.1)
    pydirectinput.click(1732, 664)

def mount_reset():
    pydirectinput.press('x')
    # May need to add a wait here.
    # This also might be able to just be deleted.
    #pydirectinput.press('x')

def dragon_bombardment():
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')

def glide(jumps):
    pydirectinput.keyDown('space')
    glide_time = jumps * 3 - (jumps/3)
    end_time = time.time() + glide_time
    # To stop yourself from removing our mount before gliding can start.
    time.sleep(1)
    while time.time() < end_time:
        dragon_bombardment()
    pydirectinput.keyUp('space')

def fall(jumps):
    mount_reset()
    #given (jumps/3)
    end_time = time.time() + (jumps/3)
    while time.time() < end_time:
        continue

def jump(jumps):
    pydirectinput.press('z')
    for i in range(jumps):
        pydirectinput.press('space')
    # Maybe we call glide right after?

def run(jumps, stop_event):
    while not stop_event.is_set():
        #How long until we go to another world. Getting stuck is going to happen A L O T.
        minutes = 5

        # Getting our time ready, 60 seconds * minutes
        #world_change_time = time.time() + (60*minutes)

        #Dragon block farm loop time!
        #I found we get stuck so much, it may be better to just reset every time.
        #while time.time() < world_change_time:
        mount_reset()
        jump(jumps)
        glide(jumps)
        fall(jumps)

        #Time to reload the world, incase we are stuck.
        world_reload()

        # wait like 10 seconds for the world to swap over.
        wait_time = time.time() + 10
        while time.time() < wait_time:
            continue

# On start
print("Press q to quit.")

# All players can at least jump 2.
print("Note, must be greater then 1")
print("Please enter the max jumps your player can do, or you want: ")
jumps = input()
jumps = int(jumps)

# Bad input check loop.
while jumps < 1:
    print("INVALID INPUT")
    print("Please enter the max jumps your player can do, or you want: ")
    jumps = input()
    jumps = int(jumps)

print("You have 3 seconds to enter your application...")
time.sleep(3)
print("Running...")

# Create a stop event for the main thread
stop_event = threading.Event()

# Makes stopping the program run on its own thread.
thread = threading.Thread(target=run, args=(jumps, stop_event))
thread.start()

#THIS IS NOT WORKING
# Wait for user input to end script.
keyboard.wait('q')

# Set the stop event to end the main thread
stop_event.set()

# Wait for the main thread to finish
thread.join()
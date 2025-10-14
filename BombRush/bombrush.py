import pyautogui
import pydirectinput
import keyboard
import time
import random

def aim_at_player():
    color = (240, 20, 20)
    s = pyautogui.screenshot()
    for x in range(s.width):
        for y in range(s.height):
            pixel = s.getpixel((x, y))
            if pixel[0] >= color[0] and \
                    pixel[1] <  color[1] and \
                    pixel[2] < color[2]:
                print("Found player at",x,y)
                pydirectinput.moveTo(x, y, relative=True)
                pyautogui.mouseDown(button='left')
                pyautogui.mouseUp(button='left')
                break
        else:  # <---this is the key.
            continue
        break

def random_keyboard_spam():
    pass
    # Check if we are in bomb rush still
        # Check if our hp, pixel has on down
            # If Our hp pixel went down, get funky!

# TOP LEFT, TOP RIGHT, BOTTOM LEFT, BOTTOM RIGHT
pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False
print("Press q to quit.")
time.sleep(3)
requeue_time = time.time()
hub_time = time.time()
try:
    while not keyboard.is_pressed('q'):
        if time.time() - requeue_time  > random.uniform(3.0,6.0):
            requeue_time = time.time()
            #Check if we need to restart the match.
            try:
                # Box(left=1330, top=817, width=91, height=18)
                rematch = pyautogui.locateOnScreen("requeue.png", confidence=0.99) # confidence=0.5
                pyautogui.click(rematch)
                last_time = time.time()
            except:
                print("No rematch found.")
                try:
                    # Go back to bomb rush.
                    in_bomb_royal = pyautogui.locateOnScreen("hub_check.png", confidence=.9)
                    if in_bomb_royal:
                        print("Not at hub.")
                except:
                    if time.time() - hub_time > 60:
                        hub_time = time.time()
                        pydirectinput.keyDown('ctrl')
                        pydirectinput.press('b')
                        pydirectinput.keyUp('ctrl')
                        # Click yes
                        time.sleep(0.5)
                        pydirectinput.click(870, 560)
                #cur_time = time.time()
                #if cur_time - last_time > 480:
                    #pass

            #Check if there is a red name tag nearby.
            try:
                aim_at_player()
            except:
                print("Player aimer broke.")

except KeyboardInterrupt:
    print('\nStopped by user.')


"""
# This match was way too long, reset time.
                #Reset timer
                last_time = cur_time
                #Open Atlas
                pyautogui.keyDown('ctrl')
                pyautogui.press('a')
                pyautogui.keyUp('ctrl')
                #Let the game breath.
                time.sleep(1)
                #Click the return home button
                #x1680 y700
                pyautogui.click(1680,700)
                #Let the game load
                time.sleep(15)
                #Go back to bomb rush.
                pyautogui.keyDown('ctrl')
                pyautogui.press('b')
                pyautogui.keyUp('ctrl')
                #x870 y560
                pyautogui.click(870, 560)
"""
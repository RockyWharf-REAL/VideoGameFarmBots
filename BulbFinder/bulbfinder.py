import random

import keyboard
import pyautogui
import threading

import pydirectinput
from PIL import Image
#from torchvision.ops import boxes
from ultralytics import YOLO
import time

decision = {
    "bulb": False
}

def screenshot_finder_test():
    # Take Screenshot
    screenshot = pyautogui.screenshot()
    # Convert Screenshot
    screenshot = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())

    # Try to Find all bulbs (hopefully) on screen
    model([screenshot], conf=.3, save=True) # Yippe, it works :)

def find_bulbs():
    # Take Screenshot
    screenshot = pyautogui.screenshot()
    # Convert Screenshot
    screenshot = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())

    # Try to Find all bulbs (hopefully) on screen
    results = model([screenshot], conf=0.25, save=False)
    return results

def rep_cam():
    pydirectinput.press('space')
    time.sleep(0.1)
    pydirectinput.press('space')
    time.sleep(0.1)
    pydirectinput.press('space')


def best_camera_angle_search_for_bulb():
    pydirectinput.moveTo(pyautogui.position().x, 2000, relative=True)
    pydirectinput.moveTo(pyautogui.position().x + 150, -60, relative=True)
    thread = threading.Thread(target=rep_cam)
    thread.start()

def main():
    # Bot code
    requeue_time = time.time()
    while True:
        if time.time() - requeue_time  < 0.05:
            continue
        requeue_time = time.time()

        # We want to stop the program when we press q
        if keyboard.is_pressed('q'):
            pydirectinput.keyUp('w')
            break

        # Get our data
        find_bulb_thread = threading.Thread(target=find_bulbs)
        results = find_bulbs()
        result = results[0]
        if len(result.boxes) == 0:
            print("Objects not found")
            best_camera_angle_search_for_bulb()
            continue

        # Calculate area for each bounding box and find the largest one
        boxes = result.boxes.xyxy.tolist()
        areas = [(box[2] - box[0]) * (box[3] - box[1]) for box in boxes]
        best_idx = max(range(len(areas)), key=lambda i: areas[i])

        # Get the best detection details
        best_class_id = int(result.boxes.cls[best_idx].cpu().numpy())
        best_class_name = result.names[best_class_id]
        best_box = result.boxes.xyxy[best_idx].cpu().numpy()  # [x1, y1, x2, y2]

        # Calculate center position
        x1, y1, x2, y2 = best_box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        pydirectinput.moveTo(int(center_x), int(center_y) + 50, relative=True)

# Load a model
model = YOLO("Datasets/v2/best.pt")

# Time to move over to the program.
time.sleep(2)

print("Press q to quit.")
pydirectinput.keyDown('w')
main()
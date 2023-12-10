import pyautogui #
import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk

time.sleep(2)

toggle_key = KeyCode(char='`')
clicking = False
mouse = Controller()

def clicker(x, y):
    while True:
        if clicking:
            mouse.click(Button.left, 1)
            print("Turned on")
        time.sleep(np.random.uniform(x, y))

def toggle_event(key):
    if key == toggle_key:
        global clicking
        clicking = not clicking
        print("Turned off")

click_thread = threading.Thread(target=clicker, args=(0.1, 0.1))
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()


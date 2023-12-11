import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk

class Autoclicker:
    def __init__(self, master):
        self.delay = (0.1, 0.1)
        self.default_hotkey = KeyCode(char='`')
        self.option_hotkey = ['`', 'F1', 'F2']
        self.clicking = False
        self.mouse = Controller()

        # GUI setup
        self.master = master
        self.master.title("Autoclicker")

        # Welcome Label
        self.welcome_label = tk.Label(master, text="Welcome to Autoclicker", font=("Arial", 15))
        self.welcome_label.pack()

        # Credits
        self.credits_label = tk.Label(master, text="By Gor Mar", font=("Arial", 10))
        self.credits_label.pack()

        click_thread = threading.Thread(target=self.clicker, args=self.delay)
        click_thread.start()

        with Listener(on_press=self.toggle_event) as listener:
            listener.join()

    def clicker(self, x, y):
        while True:
            if self.clicking:
                self.mouse.click(Button.left, 1)
                print("Turned on")
            time.sleep(np.random.uniform(x, y))

    def toggle_event(self, key):
        if self.default_hotkey == key:
            self.clicking = not self.clicking
            print("Turned off" if not self.clicking else "Turned on")

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("350x200")
    root.mainloop()
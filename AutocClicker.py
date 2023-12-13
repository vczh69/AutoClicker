import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk
from tkinter import ttk

class Autoclicker:
    def __init__(self, master):
        self.delay = (0.1, 0.1)
        self.hotkey = KeyCode(char='`')
        self.hotkey_options = ['`', 't', 'r']
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

        # Hotkey dropdown menu
        self.select_label = tk.Label(master, text="Select hotkey:", font=("Arial", 15))
        self.select_label.pack(pady=5)
        
        self.hotkey_var = tk.StringVar(master, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(master, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 15))
        self.hotkey_combobox.pack(pady=5)

        # Create thread for GUI
        self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.daemon = True 
        self.gui_thread.start()

        # Create thread for autoclicker
        self.click_thread = threading.Thread(target=self.clicker, args=(self.delay,))
        self.click_thread.daemon = True
        self.click_thread.start()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_gui(self):
        with Listener(on_press=self.toggle_event) as listener:
            listener.join()

    def clicker(self, delay):
        x, y = delay
        while True:
            if self.clicking:
                self.mouse.click(Button.left, 1)
                print("Turned on")
            time.sleep(np.random.uniform(x, y))

    def toggle_event(self, key):
        pressed_key = str(key).replace("'", "")
        selected_hotkey = str(self.hotkey_var.get())

        if pressed_key == selected_hotkey:
            self.clicking = not self.clicking
            print("Turned off" if not self.clicking else "Turned on")

    def on_close(self):
        self.clicking = False
        time.sleep(1)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("350x200")
    root.mainloop()
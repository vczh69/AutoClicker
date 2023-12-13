import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk
from tkinter import ttk

class Autoclicker:
    def __init__(self, master):
        self.delay = 1
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

        self.cps_entry = tk.Entry(master)
        self.cps_label = tk.Label(master, text="Enter CPS:", font=("Arial", 15))
        self.cps_label.pack(pady=5)
        self.cps_entry.pack()

        # Hotkey dropdown menu
        self.select_label = tk.Label(master, text="Select hotkey:", font=("Arial", 15))
        self.select_label.pack( pady=5)
        
        # Set the default value as the character representation of hotkey.char
        self.hotkey_var = tk.StringVar(master, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(master, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 15))
        self.hotkey_combobox.pack(pady=5)

        # Save button
        self.save_button = tk.Button(master, text="Save", command=self.update_cps)
        self.save_button.pack(pady=5)

        # Create thread for GUI
        self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.daemon = True 
        self.gui_thread.start()

        # Create thread for autoclicker
        self.click_thread = threading.Thread(target=self.clicker)
        self.click_thread.daemon = True
        self.click_thread.start()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_gui(self):
        with Listener(on_press=self.toggle_event) as listener:
            listener.join()

    def clicker(self):
        while True:
            start_time = time.time()

            if self.clicking:
                self.mouse.click(Button.left, 1)
                print("Turned on")

            execution_time = time.time() - start_time
            sleep_time = max(0, self.delay - execution_time)

            time.sleep(sleep_time)

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

    def update_cps(self):
        try:
            cps = float(self.cps_entry.get())
            if cps > 0:
                self.delay = 1 / cps
                print(f"CPS updated to {cps}")
            else:
                print("Please enter a valid CPS value greater than 0.")
        except ValueError:
            print("Please enter a valid numerical CPS value.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("350x300")
    root.mainloop()
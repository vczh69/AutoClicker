import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk
from tkinter import ttk

class Autoclicker:
    def __init__(self, master):
        self.label_created = False
        self.clicking = False
        self.delay = 1
        self.hotkey = KeyCode(char='`')
        self.hotkey_options = ['`', 't', 'r']
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

        # CPS entry
        self.cps_label = tk.Label(master, text="Enter CPS:", font=("Arial", 15))
        self.cps_label.pack(pady=5)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.cps_entry = tk.Entry(master, validate="key", validatecommand=vcmd)
        self.cps_entry.pack(pady=10)

        # Hotkey dropdown menu
        self.select_label = tk.Label(master, text="Select hotkey:", font=("Arial", 15))
        self.select_label.pack( pady=5)
        
        self.hotkey_var = tk.StringVar(master, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(master, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 15))
        self.hotkey_combobox.pack(pady=10)

        # Save button
        self.save_button = tk.Button(master, text="Save", command=self.update_cps, font=("Arial", 15))
        self.save_button.pack(pady=6)

        # Create thread for GUI
        self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.daemon = True 
        self.gui_thread.start()

        # Create thread for autoclicker
        self.click_thread = threading.Thread(target=self.clicker)
        self.click_thread.daemon = True
        self.click_thread.start()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def validate_input(self, value):
        if not value:
            return True

        return len(value) <= 4 and value.replace('.', '', 1).isdigit()

    def setup_gui(self):
        with Listener(on_press=self.toggle_event) as listener:
            listener.join()

    def clicker(self):
        while True:
            start_time = time.time()

            if self.clicking:
                self.mouse.click(Button.left, 1)

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
        time.sleep(0.5)
        self.master.destroy()

    def update_cps(self):
        try:
            cps = float(self.cps_entry.get())
            if cps > 0:
                self.delay = 1 / cps
            self.error_label.pack_forget()
            print(f"CPS updated to {cps}")
        except ValueError:
            if not self.label_created:
                self.error_label = tk.Label(self.master, text="Enter a valid CPS", font={"Arial", 10})
                self.error_label.pack(pady=5)
                self.label_created = True
                print("label created")

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("350x300")
    root.mainloop()
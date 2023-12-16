import time
import numpy as np
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import tkinter as tk
from tkinter import ttk

class Autoclicker:
    def __init__(self, master):
        self.cps = 10
        self.clicking = False
        self.delay = 1
        self.hotkey = KeyCode(char='t')
        self.hotkey_options = ['t', '`', 'r']
        self.mouse = Controller()

        # GUI setup
        self.master = master
        self.master.title("Autoclicker by Gor Mar")

        # Click button
        click_style = ttk.Style()
        click_style.configure("Click.TButton", font=("Arial", 15))

        self.click_button = ttk.Label(master, style="Click.TButton", text=f"Press {self.hotkey} to start clicking \nwith {self.cps} CPS" 
                                       if not self.clicking else f"Press {self.hotkey} to stop clicking")
        self.click_button.pack(pady=15)
        
        # Options button
        options_style = ttk.Style()
        options_style.configure("Options.TButton", font=("Arial", 15), width=20)

        self.options_button = ttk.Button(master, text="Options", command=self.options_window, style="Options.TButton")
        self.options_button.pack(pady=5)

        # Create thread for GUI
        self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.daemon = True 
        self.gui_thread.start()

        # Create thread for autoclicker
        self.click_thread = threading.Thread(target=self.clicker)
        self.click_thread.daemon = True
        self.click_thread.start()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def options_window(self):
        options_window = tk.Toplevel(self.master)
        options_window.title("Options")
        options_window.geometry("200x250")

        self.label_created = False

        # CPS entry
        self.cps_label = tk.Label(options_window, text="Enter CPS:", font=("Arial", 15))
        self.cps_label.pack(pady=5)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.cps_entry = tk.Entry(options_window, validate="key", validatecommand=vcmd)
        self.cps_entry.pack(pady=10)

        # Hotkey dropdown menu
        self.select_label = tk.Label(options_window, text="Select hotkey:", font=("Arial", 15))
        self.select_label.pack(pady=5)
        
        self.hotkey_var = tk.StringVar(options_window, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(options_window, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 10), width=15)
        self.hotkey_combobox.pack(pady=10)

        # Save button
        save_style = ttk.Style()
        save_style.configure("Save.TButton", font=("Arial", 15))

        self.save_button = ttk.Button(options_window, style="Save.TButton", text="Save", command=lambda: [self.update_cps(options_window), self.update_button_text()])
        self.save_button.pack(pady=6)

    def update_button_text(self):
        self.hotkey = KeyCode(char=self.hotkey_var.get())
        print(f"Hotkey updated to {self.hotkey}")
        self.click_button.configure(text=f"Press {self.hotkey} to start clicking\nwith {self.cps} CPS" if not self.clicking else f"Press {self.hotkey} to stop clicking")

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

    def update_cps(self, options_window):
        try:
            self.cps = float(self.cps_entry.get())
            if self.cps > 0:
                self.delay = 1 / self.cps
            if self.label_created:
                self.error_label.pack_forget()
            self.saved_label = tk.Label(options_window, text="Saved", font=("Arial", 18), fg="green")
            self.saved_label.pack(pady=5)
            print(f"CPS updated to {self.cps}")
        except ValueError:
            if not self.label_created:
                self.error_label = tk.Label(options_window, text="Enter a valid CPS", font={"Arial", 10}, fg="red")
                self.error_label.pack(pady=5)
                self.label_created = True
                print("label created")

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("250x150")
    root.mainloop()
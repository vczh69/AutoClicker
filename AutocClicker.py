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
        self.listener = None

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

    def setup_gui(self):
        self.listener = Listener(on_press=self.toggle_event)
        self.listener.start()
        self.listener.join()

    def options_window(self):
        options_window = tk.Toplevel(self.master)
        options_window.title("Options")
        options_window.geometry("300x250")
        frame = ttk.Frame(options_window)
        frame.grid(row=0, column=0)
        self.label_created = False

        # CPS entry
        self.cps_frame = tk.LabelFrame(frame, text="CPS", font=("Arial", 15))
        self.cps_frame.grid(row=0, column=0, padx=20, pady=10)

        self.accept_var = tk.StringVar(value="No")
        self.det_risk = tk.Checkbutton(self.cps_frame, text="Lower\ndetection risk",
                                        variable=self.accept_var, onvalue="Yes", offvalue="No")
        self.det_risk.grid(row=0, column=0)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.cps_entry = tk.Entry(self.cps_frame, validate="key", validatecommand=vcmd)
        self.cps_entry.grid(row=0, column=1, pady=10, padx=10)

        # Hotkey dropdown menu
        self.hotkey_frame = tk.LabelFrame(frame, text="Hotkey", font=("Arial", 15))
        self.hotkey_frame.grid(row=1, column=0, padx=20, pady=10)

        self.select_label = tk.Label(self.hotkey_frame, text="Select hotkey:")
        self.select_label.grid(row=0, column=0, pady=10, padx=10)

        self.hotkey_var = tk.StringVar(self.hotkey_frame, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(self.hotkey_frame, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 10), width=15)
        self.hotkey_combobox.grid(row=0, column=1, pady=10, padx=10)

        # Save button
        save_style = ttk.Style()
        save_style.configure("Save.TButton", font=("Arial", 15))

        self.save_button = ttk.Button(options_window, style="Save.TButton", text="Save", command=lambda: [self.update_cps(options_window), self.update_button_text()])
        self.save_button.grid(row=1, column=0, pady=6)

        if self.listener and self.listener.is_alive():
            self.listener.stop()

    def update_button_text(self):
        if self.listener and not self.listener.is_alive():
            self.listener = Listener(on_press=self.toggle_event)
            self.listener.start()

        self.hotkey = KeyCode(char=self.hotkey_var.get())
        print(f"Hotkey updated to {self.hotkey}")
        self.click_button.configure(text=f"Press {self.hotkey} to start clicking\nwith {self.cps} CPS" if not self.clicking else f"Press {self.hotkey} to stop clicking")

    def validate_input(self, value):
        if not value:
            return True

        return len(value) <= 4 and value.replace('.', '', 1).isdigit()

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
                self.error_label.grid_forget()
            self.saved_label = tk.Label(options_window, text="Saved", font=("Arial", 10), fg="green")
            self.saved_label.grid(pady=5)
            print(f"CPS updated to {self.cps}")
        except ValueError:
            if not self.label_created:
                self.error_label = tk.Label(options_window, text="Enter a valid CPS", font={"Arial", 10}, fg="red")
                self.error_label.grid(pady=5)
                self.label_created = True
                print("label created")

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("250x150")
    root.mainloop()
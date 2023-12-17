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
        self.cps_options = ["8-11", "9-12", "10-13", "11-14", "12-15", "13-16", "14-17", "15-18", "16-19", "17-20", "18-21", "19-22"]
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

        # CPS
        self.cps_frame = tk.LabelFrame(frame, text="CPS", font=("Arial", 15))
        self.cps_frame.grid(row=0, column=0, padx=20, pady=10)

        self.det_risk_var = tk.StringVar(value="No")
        self.det_risk = tk.Checkbutton(self.cps_frame, text="Lower\ndetection risk",
                                        variable=self.det_risk_var, onvalue="Yes", offvalue="No")
        self.det_risk.grid(row=0, column=0)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.cps_entry = ttk.Spinbox(self.cps_frame, from_=1, to=100, validate="key", validatecommand=vcmd)
        self.cps_entry.grid(row=0, column=1, pady=10, padx=10)

        # Hotkey
        self.hotkey_frame = tk.LabelFrame(frame, text="Hotkey", font=("Arial", 15))
        self.hotkey_frame.grid(row=1, column=0, padx=20, pady=10)

        self.select_label = tk.Label(self.hotkey_frame, text="Select hotkey:")
        self.select_label.grid(row=0, column=0, pady=10, padx=10)

        self.hotkey_var = tk.StringVar(self.hotkey_frame, value=self.hotkey.char)
        self.hotkey_combobox = ttk.Combobox(self.hotkey_frame, textvariable=self.hotkey_var, values=self.hotkey_options, state="readonly", font=("Arial", 10), width=15)
        self.hotkey_combobox.grid(row=0, column=1, pady=10, padx=10)
    
        self.det_risk_var.trace_add('write', lambda *args, **kwargs: self.update_det_risk())

        # Save button
        save_style = ttk.Style()
        save_style.configure("Save.TButton", font=("Arial", 15), width=22)

        self.save_button = ttk.Button(options_window, style="Save.TButton", text="Save", command=lambda: [self.update_det_risk(options_window), self.update_cps(options_window), self.update_button_text()])
        self.save_button.grid(row=1, column=0, pady=6)

        if self.listener and self.listener.is_alive():
            self.listener.stop()

    def update_det_risk(self, *args, **kwargs):
        self.low_det_risk = self.det_risk_var.get()
        if self.low_det_risk == "No":
            self.cps_entry.grid(row=0, column=1, pady=10, padx=10)

            if hasattr(self, 'cps_dropdown'):
                self.cps_dropdown.grid_forget()
        else:
            self.cps_entry.grid_forget()

            if not hasattr(self, 'cps_dropdown'):
                self.cps_dropdown = ttk.Combobox(self.cps_frame, values=self.cps_options, state="readonly")

            self.cps_dropdown.grid(row=0, column=1, pady=10, padx=10)
            self.update_cps_dropdown()

    def update_cps_dropdown(self):
        self.cps_range = self.cps_dropdown.get()
        if self.cps_range:
            cps_start, cps_end = map(int, self.cps_range.split('-'))
            cps_values = np.random.uniform(cps_start, cps_end, size=10)
            self.cps_values = [round(cps, 2) for cps in cps_values.tolist()]

    def update_cps(self, options_window):
        try:
            if self.low_det_risk == "No":
                self.cps = float(self.cps_entry.get())
            else:
                self.cps = np.random.choice(self.cps_values)
                
            if self.cps > 0:
                self.delay = 1 / self.cps
            if self.label_created:
                self.error_label.grid_forget()
            self.saved_label = tk.Label(options_window, text="Saved", font=("Arial", 14), fg="green")
            self.saved_label.grid()
            print(f"CPS updated to {self.cps}")
        except ValueError:
            if not self.label_created:
                self.error_label = tk.Label(options_window, text="Enter a valid CPS", font={"Arial", 10}, fg="red")
                self.error_label.grid()
                self.label_created = True
                print("label created")

    def update_button_text(self):
        if self.listener and not self.listener.is_alive():
            self.listener = Listener(on_press=self.toggle_event)
            self.listener.start()

        self.hotkey = KeyCode(char=self.hotkey_var.get())
        print(f"Hotkey updated to {self.hotkey}")
        if self.low_det_risk == "No":
            self.click_button.configure(text=f"Press {self.hotkey} to start clicking\nwith {self.cps} CPS" if not self.clicking else f"Press {self.hotkey} to stop clicking")
        else:
            self.click_button.configure(text=f"Press {self.hotkey} to start clicking\nwith {self.cps_range} CPS" if not self.clicking else f"Press {self.hotkey} to stop clicking")   
    
    def validate_input(self, value):
        if not value:
            return True

        try:
            num = float(value)
            int_part, _, frac_part = value.partition('.')
            return 0 <= num <= 100 and len(int_part) <= 3 and len(frac_part) <= 2
        except ValueError:
            return False

    def clicker(self):
        while True:
            start_time = time.time()

            if self.clicking:
                if self.low_det_risk == "Yes":
                    self.delay = 1 / self.cps
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

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("250x150")
    root.mainloop()
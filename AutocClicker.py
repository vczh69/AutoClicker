import time
import numpy as np
from pynput.mouse import Controller, Button
import keyboard
import threading
import tkinter as tk
from tkinter import ttk

class Autoclicker:
    def __init__(self, master):
        self.cps_range = "10-13"
        self.cps = 1.0
        self.delay = 1
        self.hotkey = 't'
        self.clickingkey = "LMB"
        self.clickingkey_options = ["LMB", "RMB", "MMB"]
        self.cps_options = ["8-11", "9-12", "10-13", "11-14", "12-15", "13-16", "14-17", "15-18", "16-19", "17-20", "18-21", "19-22"]
        self.low_det_risk = "No"
        self.mouse = Controller()
        self.clicking = False
        self.recording = False

        frame = ttk.Frame(master)
        frame.grid(row=0, column=0)

        # GUI setup
        self.master = master
        self.master.title("Autoclicker by Gor Mar")

        # Info
        self.info_frame = tk.LabelFrame(frame, text="Info", font=("Arial", 15))
        self.info_frame.grid(row=0, column=0, padx=20, pady=10)

        info_style = ttk.Style()
        info_style.configure("Info.TButton", font=("Arial", 12))

        self.info_label = ttk.Label(self.info_frame, style="Info.TButton", text=f"Press {self.hotkey} to start clicking\n{self.clickingkey} with {self.cps} CPS")
        self.info_label.grid(row=0, column=0, padx=10, pady=5)

        # CPS
        self.cps_frame = tk.LabelFrame(frame, text="CPS", font=("Arial", 15))
        self.cps_frame.grid(row=0, column=1, padx=20, pady=10)

        self.det_risk_var = tk.StringVar(value="No")
        self.det_risk = tk.Checkbutton(self.cps_frame, text="Lower\ndetection risk",
                                        variable=self.det_risk_var, onvalue="Yes", offvalue="No")
        self.det_risk.grid(row=0, column=0)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.cps_spinbox = ttk.Spinbox(self.cps_frame, from_=1, to=100, validate="key", validatecommand=vcmd)
        self.cps_spinbox.grid(row=0, column=1, pady=10, padx=10)

        self.cps_spinbox.delete(0, tk.END)
        self.cps_spinbox.insert(0, "1") 

        # Clicking Key
        self.clickingkey_frame = tk.LabelFrame(frame, text="Clicking Key", font=("Arial", 15))
        self.clickingkey_frame.grid(row=1, column=0, padx=20, pady=10)

        self.clickingkey_label = tk.Label(self.clickingkey_frame, text="Select\n Clicking Key:")
        self.clickingkey_label.grid(row=0, column=0, pady=10, padx=10)

        self.clickingkey_var = tk.StringVar(value=self.clickingkey)
        self.clickingkey_combobox = ttk.Combobox(self.clickingkey_frame, textvariable=self.clickingkey_var, values=self.clickingkey_options, state="readonly", font=("Arial", 10), width=10)
        self.clickingkey_combobox.grid(row=0, column=1, pady=10, padx=10)

        # Hotkey
        self.hotkey_frame = tk.LabelFrame(frame, text="Hotkey", font=("Arial", 15))
        self.hotkey_frame.grid(row=1, column=1, padx=20, pady=10)

        record_style = ttk.Style()
        record_style.configure("Record.TButton", font=("Arial", 11))

        self.record_button = ttk.Button(self.hotkey_frame, style="Record.TButton", text="Record", command=self.record_button_click)
        self.record_button.grid(padx=5)

        self.hotkey_var = tk.StringVar(value=self.hotkey)
        self.hotkey_combobox = ttk.Entry(self.hotkey_frame, textvariable=self.hotkey_var, state="readonly", font=("Arial", 10), width=10)
        self.hotkey_combobox.grid(row=0, column=1, pady=10, padx=10)

        self.det_risk_var.trace_add('write', lambda *args, **kwargs: self.update_det_risk())

        # Save button
        save_style = ttk.Style()
        save_style.configure("Save.TButton", font=("Arial", 15), width=22)

        self.save_button = ttk.Button(master, style="Save.TButton", text="Save", command=lambda: [self.update_det_risk(), self.update_cps(), self.update_button_text(), self.start_cps_updates()])
        self.save_button.grid(row=2, column=0, columnspan=2, pady=2)

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
        keyboard.hook(self.toggle_event)

    def start_cps_updates(self):
        random_delay = np.random.uniform(2, 4)
        self.master.after(int(random_delay * 1000), self.update_cps_periodically)

    def record_button_click(self):
        if not self.recording:
            self.record_button.configure(text="Recording...")
            self.hotkey_var.set("")
            self.recording = True
            self.save_button['state'] = 'disabled'
            self.record_button['state'] = 'disabled'
        else:
            self.record_button.configure(text="Record")
            self.recording = False

    def update_cps_periodically(self):
        if self.low_det_risk == "Yes":
            self.update_cps()
            self.start_cps_updates()

    def update_det_risk(self, *args, **kwargs):
        self.low_det_risk = self.det_risk_var.get()
        if self.low_det_risk == "No":
            self.cps_spinbox.grid(row=0, column=1, pady=10, padx=10)

            if hasattr(self, 'cps_dropdown'):
                self.cps_dropdown.grid_forget()
        else:
            self.cps_spinbox.grid_forget()

            if not hasattr(self, 'cps_dropdown'):
                self.cps_dropdown = ttk.Combobox(self.cps_frame, values=self.cps_options, state="readonly")
                self.cps_dropdown.set("10-13") 

            self.cps_dropdown.grid(row=0, column=1, pady=10, padx=10)

    def update_cps(self):
        if self.low_det_risk == "No":
            self.cps = float(self.cps_spinbox.get())
        else:
            self.cps_range = self.cps_dropdown.get()
            if self.cps_range:
                cps_start, cps_end = map(int, self.cps_range.split('-'))
                self.cps = round(np.random.uniform(cps_start, cps_end), 2)
            
        if self.cps > 0:
            self.delay = 1 / self.cps
        print(f"CPS updated to {self.cps}")

    def update_button_text(self):

        self.hotkey = self.hotkey_var.get()
        self.clickingkey = self.clickingkey_var.get()

        print(f"Hotkey updated to {self.hotkey}, Clicking key updated to {self.clickingkey}")
        self.update_info_label()

    def update_info_label(self):
        if self.low_det_risk == "No":
            self.info_label.configure(text=f"Press {self.hotkey} to {'start' if self.clicking else 'stop'} clicking\n{self.clickingkey} with {self.cps} CPS")
        else:
            self.info_label.configure(text=f"Press {self.hotkey} to {'start' if self.clicking else 'stop'} clicking\n{self.clickingkey} with {self.cps_range} CPS")
    
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

                if self.clickingkey == "LMB":
                    self.mouse.click(Button.left, 1)
                elif self.clickingkey == "RMB":
                    self.mouse.click(Button.right, 1)
                elif self.clickingkey == "MMB":
                    self.mouse.click(Button.middle, 1)

            execution_time = time.time() - start_time
            sleep_time = max(0, self.delay - execution_time)

            time.sleep(sleep_time)

    def toggle_event(self, e):
        if self.recording:
            self.hotkey_var.set(e.name)
            self.save_button['state'] = 'normal'
            self.record_button['state'] = 'normal'
            self.record_button.configure(text="Record")
            self.recording = False
            return

        if keyboard.is_pressed(self.hotkey):
            self.update_info_label()
            self.clicking = not self.clicking

    def on_close(self):
        self.clicking = False
        time.sleep(0.5)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Autoclicker(root)
    root.geometry("560x250")
    root.mainloop()
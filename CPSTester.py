import tkinter as tk
from tkinter import ttk

class CPSTester:
    def __init__(self, master):
        self.label_created = False
        self.click_count = 0
        self.duration_options = [1, 5, 10, 30, 60, 120, 300]
        self.start_duration = self.duration_options[0]
        self.duration = self.start_duration

        # GUI setup
        self.master = master
        self.master.title("CPS Tester by Gor Mar")

        # Duration entry
        style = ttk.Style()
        style.configure("TEntry")

        self.duration_label = tk.Label(master, text="Enter duration:", font=("Arial", 15))
        self.duration_label.pack(pady=10)

        vcmd = (self.master.register(self.validate_input), '%P')
        self.duration_entry = ttk.Entry(master, validate="key", validatecommand=vcmd, style="TEntry", width=20)
        self.duration_entry.pack(pady=5)

        # Start button
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 18))

        self.start_button = ttk.Button(master, text="Start", command=self.start_timer, style="TButton", width=10)
        self.start_button.pack(pady=10)

    def validate_input(self, value):
        if not value:
            return True

        return len(value) <= 4 and value.replace('.', '', 1).isdigit()

    def start_timer(self):
        try:
            self.start_duration = float(self.duration_entry.get())
            self.duration = self.start_duration
            self.start_button.pack_forget() 
            self.duration_entry.pack_forget()
            self.duration_label.pack_forget()
            if self.label_created:
                self.error_label.pack_forget()

            # Click button
            style = ttk.Style()
            style.configure("TButton", font=("Arial", 20),  width=15, height=1, borderwidth=2)

            self.label = tk.Label(self.master, text=f"Click count: 0\n\nTime remaining: {self.duration:.1f} seconds", font=("Arial", 14))
            self.label.pack(pady=20)

            self.click_button = ttk.Button(self.master, text="Click", command=self.increment_click_count, style="TButton")
            self.click_button.pack()
        except ValueError:
            if not self.label_created:
                self.error_label = tk.Label(self.master, text="Enter a valid duration", font={"Arial", 3}, fg="red")
                self.error_label.pack(pady=5)
                self.label_created = True
                print("label created")

    def increment_click_count(self):
        if self.click_count == 0:
            self.update_timer() 
        self.click_count += 1
        self.label.config(text=f"Click count: {self.click_count}\n\nTime remaining: {self.duration:.1f} seconds")

    def update_timer(self):
        if self.duration > 0:
            self.duration -= 0.1
            self.duration = max(0, self.duration)
            self.label.config(text=f"Click count: {self.click_count}\n\nTime remaining: {self.duration:.1f} seconds")
            self.master.after(100, self.update_timer)
        else:
            self.click_button.pack_forget()
            self.cps()

    def cps(self, current_cps=None):
        if current_cps is None:
            current_cps = 0
        if self.start_duration > 0:
            cps = self.click_count / self.start_duration
        else: 
            cps = 0 

        if current_cps < cps:
            current_cps += 0.1
            current_cps = min(cps, current_cps)
            self.label.config(text=f"Final click count: {self.click_count}\n\nCPS: {current_cps:.2f}")
            self.master.after(10, self.cps, current_cps)
        else:
            # Restart button
            restart_style = ttk.Style()
            restart_style.configure("Restart.TButton", font=("Arial", 15), width=8)

            self.restart_button = ttk.Button(self.master, text="Restart", command=self.restart_game, style="Restart.TButton")
            self.restart_button.pack(side=tk.LEFT, padx=20, pady=10)

            # Exit button
            exit_style = ttk.Style()
            exit_style.configure("Exit.TButton", font=("Arial", 15), width=5)

            self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy, style="Exit.TButton")
            self.exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def restart_game(self):
        self.label.pack_forget()
        self.restart_button.pack_forget()
        self.exit_button.pack_forget()
        self.__init__(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = CPSTester(root)
    root.geometry("350x180")
    root.mainloop()

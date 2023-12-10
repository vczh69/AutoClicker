import tkinter as tk
from tkinter import ttk

class CPSTester:
    def __init__(self, master):
        # Name
        self.master = master
        self.master.title("CPS Tester")

        # Values
        self.click_count = 0
        self.duration_options = [1, 5, 10, 30, 60, 120, 300]
        self.start_duration = self.duration_options[0]
        self.duration = self.start_duration

        # Welcome Label
        self.welcome_label = tk.Label(master, text="Welcome to CPS Tester", font=("Arial", 15))
        self.welcome_label.pack()

        # Credits
        self.credits_label = tk.Label(master, text="By Gor Mar", font=("Arial", 10))
        self.credits_label.pack()

        # Label for dropdown menu
        self.select_label = tk.Label(master, text="Select duration:", font=("Arial", 15))
        self.select_label.pack(pady=5)

        # Duration dropdown menu
        self.duration_var = tk.StringVar(master)
        self.duration_var.set(self.start_duration) 
        self.duration_combobox = ttk.Combobox(master, textvariable=self.duration_var, values=self.duration_options, state="readonly", font=("Arial", 15))
        self.duration_combobox.pack(pady=5)

        # Start button
        self.start_button = tk.Button(master, text="Start", command=self.start_timer, font=("Arial", 15))
        self.start_button.pack(pady=5)

    def start_timer(self):
        self.start_duration = float(self.duration_var.get())
        self.duration = self.start_duration
        self.start_button.pack_forget() 
        self.duration_combobox.pack_forget()
        self.select_label.pack_forget()
        self.welcome_label.pack_forget()
        self.credits_label.pack_forget()

        self.label = tk.Label(self.master, text=f"Click count: 0\nTime remaining: {self.duration:.1f} seconds", font=("Arial", 14))
        self.label.pack(pady=20)

        self.click_button = tk.Button(self.master, text="Click me!", command=self.increment_click_count, font=("Arial", 20))
        self.click_button.pack()

    def increment_click_count(self):
        if self.click_count == 0:
            self.update_timer() 
        self.click_count += 1
        self.label.config(text=f"Click count: {self.click_count}\nTime remaining: {self.duration:.1f} seconds")

    def update_timer(self):
        if self.duration > 0:
            self.duration -= 0.1
            self.label.config(text=f"Click count: {self.click_count}\nTime remaining: {self.duration:.1f} seconds")
            self.master.after(100, self.update_timer) 
        else:
            self.click_button.pack_forget()
            cps = self.click_count / self.start_duration
            self.label.config(text=f"Final click count: {self.click_count}\n\nCPS: {cps:.2f}", font=("Arial", 15))

            # Restart button
            self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game, font=("Arial", 15))
            self.restart_button.pack(pady=10)

    def restart_game(self):
        self.label.pack_forget()
        self.restart_button.pack_forget()
        self.__init__(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = CPSTester(root)
    root.geometry("350x200")
    root.mainloop()

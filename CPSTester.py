import tkinter as tk

class CPSTester:
    def __init__(self, master):
        # Name
        self.master = master
        self.master.title("CPS Tester")

        # Values
        self.click_count = 0
        self.start_duration = 10
        self.duration = 10

        # Duration
        self.duration_entry = tk.Entry(master)
        self.duration_entry.insert(0, str(self.start_duration))
        self.duration_entry.pack(pady=10)

        # Start button
        self.start_button = tk.Button(master, text="Start", command=self.start_timer, font=("Arial", 12))
        self.start_button.pack()

    def start_timer(self):
        try:
            self.start_duration = float(self.duration_entry.get())
            self.duration = self.start_duration
            self.start_button.pack_forget()  # Remove the Start button
            self.duration_entry.pack_forget()  # Remove the duration entry

            self.label = tk.Label(self.master, text=f"Click count: 0\nTime remaining: {self.duration:.1f} seconds", font=("Arial", 14))
            self.label.pack(pady=20)

            self.click_button = tk.Button(self.master, text="Click me!", command=self.increment_click_count, font=("Arial", 20))
            self.click_button.pack()
        except ValueError:
            self.start_button.pack() 
            self.duration_entry.pack()
            self.label.config(text="Invalid input for duration")

    def increment_click_count(self):
        if self.click_count == 0:  # Check if it's the first click
            self.update_timer()  # Start the timer only on the first click
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
            self.label.config(text=f"Final click count: {self.click_count}\nCPS: {cps:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CPSTester(root)
    root.geometry("400x300")
    root.mainloop()



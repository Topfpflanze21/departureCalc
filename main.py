import tkinter as tk
import datetime


class WorkTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Workday Departure Calculator")
        self.geometry("330x250")
        self.resizable(False, False)

        # --- Variables with trace for auto-updating ---
        self.arrival_var = tk.StringVar(value="07:45")
        self.work_duration_var = tk.StringVar(value="8")
        self.lunch_break_var = tk.StringVar(value="30")

        # Add traces to call _update_calculation whenever a variable is written to
        self.arrival_var.trace_add("write", self._update_calculation)
        self.work_duration_var.trace_add("write", self._update_calculation)
        self.lunch_break_var.trace_add("write", self._update_calculation)

        self.departure_time_var = tk.StringVar(value="--:--")
        self.status_var = tk.StringVar(value="Enter your details.")
        self.current_time_var = tk.StringVar()

        self.departure_datetime = None

        # --- UI Elements ---
        self.create_widgets()

        # --- Initial Setup ---
        self._update_calculation()  # Perform initial calculation
        self.update_clock()  # Start the live clock

    def create_widgets(self):
        """Creates and places all the GUI widgets."""
        frame = tk.Frame(self, padx=15, pady=15)
        frame.pack(expand=True, fill=tk.BOTH)

        # --- Inputs ---
        tk.Label(frame, text="Arrival Time (HH:MM):").grid(row=0, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=self.arrival_var, width=15).grid(row=0, column=1, pady=3)

        tk.Label(frame, text="Work Duration (hours):").grid(row=1, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=self.work_duration_var, width=15).grid(row=1, column=1, pady=3)

        tk.Label(frame, text="Lunch Break (minutes):").grid(row=2, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=self.lunch_break_var, width=15).grid(row=2, column=1, pady=3)

        # --- Outputs ---
        separator = tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.grid(row=3, columnspan=2, sticky='ew', pady=10)

        tk.Label(frame, text="Current Time:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        tk.Label(frame, textvariable=self.current_time_var, font=("Arial", 10, "bold")).grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Departure Time:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
        tk.Label(frame, textvariable=self.departure_time_var, font=("Arial", 12, "bold"), fg="blue").grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(frame, textvariable=self.status_var, font=("Arial", 10), wraplength=300).grid(row=6, column=0, columnspan=2, pady=(10, 0))

    def _update_calculation(self, *args):
        """
        Calculates departure time based on user input.
        This method is called automatically when input variables change.
        """
        try:
            # Get inputs; use .get() which might be empty during typing
            arrival_str = self.arrival_var.get()
            work_hours_str = self.work_duration_var.get()
            lunch_minutes_str = self.lunch_break_var.get()

            # Guard against empty strings to prevent ValueErrors
            if not all([arrival_str, work_hours_str, lunch_minutes_str]):
                raise ValueError("Input field is empty")

            work_hours = int(work_hours_str)
            lunch_minutes = int(lunch_minutes_str)

            # Parse arrival time and combine with today's date
            now = datetime.datetime.now()
            arrival_time_obj = datetime.datetime.strptime(arrival_str, "%H:%M").time()
            arrival_datetime = now.replace(hour=arrival_time_obj.hour, minute=arrival_time_obj.minute, second=0, microsecond=0)

            # Calculate departure time
            work_duration = datetime.timedelta(hours=work_hours)
            lunch_duration = datetime.timedelta(minutes=lunch_minutes)
            self.departure_datetime = arrival_datetime + work_duration + lunch_duration

            # Update the departure time label
            self.departure_time_var.set(self.departure_datetime.strftime('%H:%M'))
            self.update_status()

        except ValueError:
            # Handle invalid input silently without error pop-ups
            self.departure_datetime = None
            self.departure_time_var.set("--:--")
            self.status_var.set("Waiting for valid input...")

    def update_status(self):
        """Updates the time remaining status message."""
        if not self.departure_datetime:
            return  # Do nothing if departure time isn't valid

        now = datetime.datetime.now()
        arrival_datetime = self.departure_datetime - datetime.timedelta(
            hours=int(self.work_duration_var.get()),
            minutes=int(self.lunch_break_var.get())
        )

        if now < arrival_datetime:
            self.status_var.set("Your workday has not started yet. ☀️")
        elif now >= self.departure_datetime:
            self.status_var.set("Your workday is over. Time to go home! 🎉")
        else:
            time_left = self.departure_datetime - now
            hours, remainder = divmod(time_left.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            self.status_var.set(f"Time Remaining: {int(hours)}h {int(minutes)}m ⏳")

    def update_clock(self):
        """Updates the current time and status every second."""
        self.current_time_var.set(datetime.datetime.now().strftime("%H:%M:%S"))
        self.update_status()
        self.after(1000, self.update_clock)


if __name__ == "__main__":
    app = WorkTimerApp()
    app.mainloop()
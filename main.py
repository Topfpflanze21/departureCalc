import tkinter as tk
from tkinter import ttk
import datetime


class WorkTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Basic Setup ---
        self.title("Workday Departure Calculator")
        self.minsize(500, 350)  # Set a minimum size for usability

        # --- Style Configuration ---
        style = ttk.Style(self)
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')

        # Define colors and fonts
        BG_COLOR = "#f2f2f2"
        FG_COLOR = "#333333"
        ACCENT_COLOR = "#0078d7"

        self.configure(background=BG_COLOR)
        style.configure('.', font=('Segoe UI', 10), background=BG_COLOR, foreground=FG_COLOR)
        style.configure('TLabel')
        style.configure('TEntry', padding=5)
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'))
        style.configure('Result.TLabel', font=('Segoe UI', 22, 'bold'), foreground=ACCENT_COLOR)
        style.configure('Status.TLabel', font=('Segoe UI', 10, 'italic'))
        style.configure('CurrentTime.TLabel', font=('Segoe UI', 10, 'bold'))
        # Style for the wrapper frame to ensure it inherits the background color
        style.configure('Wrapper.TFrame', background=BG_COLOR)

        # --- Variables with trace for auto-updating ---
        self.arrival_var = tk.StringVar(value="07:45")
        self.work_duration_var = tk.StringVar(value="8")
        self.lunch_break_var = tk.StringVar(value="30")

        self.arrival_var.trace_add("write", self._update_calculation)
        self.work_duration_var.trace_add("write", self._update_calculation)
        self.lunch_break_var.trace_add("write", self._update_calculation)

        self.departure_time_var = tk.StringVar(value="--:--")
        self.status_var = tk.StringVar(value="Enter your details.")
        self.current_time_var = tk.StringVar()

        self.departure_datetime = None

        # --- UI & Initial Calls ---
        self.create_widgets()
        self._update_calculation()
        self.update_clock()

    def create_widgets(self):
        """Creates and places all the GUI widgets."""
        # Main frame configured to expand with the window
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Input Frame ---
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        input_frame.columnconfigure(1, weight=1)  # Makes entry column expandable

        ttk.Label(input_frame, text="Arrival Time (HH:MM):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.arrival_var).grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(input_frame, text="Work Duration (hours):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.work_duration_var).grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(input_frame, text="Lunch Break (minutes):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.lunch_break_var).grid(row=2, column=1, sticky="ew", pady=3)

        # --- Separator ---
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # --- Output Frame (this will expand to fill space) ---
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        # --- Wrapper to keep content centered ---
        content_wrapper = ttk.Frame(output_frame, style='Wrapper.TFrame')
        content_wrapper.pack(expand=True)  # This centers the frame

        ttk.Label(content_wrapper, textvariable=self.current_time_var, style='CurrentTime.TLabel').pack()
        ttk.Label(content_wrapper, text="Estimated Departure Time", style='Header.TLabel').pack(pady=(15, 0))
        ttk.Label(content_wrapper, textvariable=self.departure_time_var, style='Result.TLabel').pack(pady=(0, 10))
        ttk.Label(content_wrapper, textvariable=self.status_var, style='Status.TLabel').pack(pady=(10, 0))

    def _update_calculation(self, *args):
        """Calculates departure time based on user input."""
        try:
            arrival_str = self.arrival_var.get()
            work_hours_str = self.work_duration_var.get()
            lunch_minutes_str = self.lunch_break_var.get()

            if not all([arrival_str, work_hours_str, lunch_minutes_str]):
                raise ValueError("Input field is empty")

            work_hours = int(work_hours_str)
            lunch_minutes = int(lunch_minutes_str)

            now = datetime.datetime.now()
            arrival_time_obj = datetime.datetime.strptime(arrival_str, "%H:%M").time()
            arrival_datetime = now.replace(hour=arrival_time_obj.hour, minute=arrival_time_obj.minute, second=0, microsecond=0)

            work_duration = datetime.timedelta(hours=work_hours)
            lunch_duration = datetime.timedelta(minutes=lunch_minutes)
            self.departure_datetime = arrival_datetime + work_duration + lunch_duration

            self.departure_time_var.set(self.departure_datetime.strftime('%H:%M'))
            self.update_status()

        except ValueError:
            self.departure_datetime = None
            self.departure_time_var.set("--:--")
            self.status_var.set("Waiting for valid input...")

    def update_status(self):
        """Updates the time remaining status message."""
        if not self.departure_datetime:
            return

        now = datetime.datetime.now()
        try:
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
        except ValueError:
            self.status_var.set("Waiting for valid input...")

    def update_clock(self):
        """Updates the current time and status every second."""
        self.current_time_var.set(datetime.datetime.now().strftime("Current Time: %H:%M:%S"))
        self.update_status()
        self.after(1000, self.update_clock)


if __name__ == "__main__":
    app = WorkTimerApp()
    app.mainloop()
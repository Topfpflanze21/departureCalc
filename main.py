import tkinter as tk
from tkinter import ttk
import datetime
import json  # Added for saving/loading settings
import sys
import os

# This function is correct, keep it as is
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- NEW: Function to get a writable path ---
def get_persistent_path(filename):
    """
    Get a writable path in the user's AppData directory for settings.
    Creates the directory if it doesn't exist.
    """
    # APPDATA is a reliable environment variable on Windows
    app_data_path = os.getenv('APPDATA')
    # Fallback to the local directory if APPDATA isn't set
    if not app_data_path:
        app_data_path = os.path.abspath(".")

    # Create a dedicated folder for your app to keep things clean
    app_folder = os.path.join(app_data_path, "WorkdayDepartureCalc")
    os.makedirs(app_folder, exist_ok=True)

    return os.path.join(app_folder, filename)

# --- Settings Paths ---
# Path for SAVING and LOADING user-specific settings
PERSISTENT_SETTINGS_FILE = get_persistent_path("settings.json")
# Path for the DEFAULT settings bundled with the app
DEFAULT_SETTINGS_FILE = resource_path("data/settings.json")

# --- Configuration Constants ---
# Grouping configuration in one place makes it easier to modify the app's appearance.
# Color Palette
BG_COLOR = "#2e2e2e"  # Dark grey background
FG_COLOR = "#e0e0e0"  # Light grey text
CARD_COLOR = "#3b3b3b"  # Slightly lighter grey for frames/cards
ACCENT_COLOR = "#00aaff"  # A vibrant blue for highlights
ENTRY_BG = "#505050"
ENTRY_FG = "#ffffff"
INVALID_BG = "#7f2a2a"  # Background color for invalid entry fields

# Font Palette
FONT_FAMILY_PRIMARY = "Segoe UI"
FONT_FAMILY_DISPLAY = "Segoe UI Variable Display"  # A more modern font for the main result

# --- Settings File ---
SETTINGS_FILE = resource_path("data/settings.json")


# --- Main Application Class ---
class WorkTimerApp(tk.Tk):
    """
    A modern desktop application to calculate the workday departure time.

    This refactored version separates initialization tasks into distinct methods
    for improved readability and maintainability.
    """

    def __init__(self):
        super().__init__()

        # --- Core Setup ---
        self.title("Workday Departure Calculator")
        self.geometry("420x520")  # Increased height slightly for new layout
        self.minsize(400, 520)
        self.configure(background=BG_COLOR)

        # Set the application icon
        self.iconphoto(True, tk.PhotoImage(file=resource_path('images/clock.png')))  # <-- Change this line

        # This will hold the calculated departure time as a datetime object
        self.departure_datetime = None

        # --- Initialization ---
        self._initialize_variables()
        self._load_settings()  # Load saved settings before creating widgets
        self._setup_styles()
        self._create_widgets()

        # --- Initial State ---
        self._recalculate_departure_time()  # Perform an initial calculation on startup
        self._update_clock()  # Start the live clock

        # --- Exit Protocol ---
        # Call the _on_closing method when the window is closed
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_styles(self):
        """Configures all the ttk styles for the application widgets."""
        style = ttk.Style(self)
        # Use the 'clam' theme as a base for its clean, modern look.
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        # --- Global Widget Styles ---
        style.configure('.',
                        background=BG_COLOR,
                        foreground=FG_COLOR,
                        font=(FONT_FAMILY_PRIMARY, 10))

        style.configure('TFrame', background=BG_COLOR)
        style.configure('Card.TFrame', background=CARD_COLOR, relief='solid', borderwidth=1)

        # --- Label Styles ---
        style.configure('TLabel', font=(FONT_FAMILY_PRIMARY, 11))
        style.configure('Header.TLabel', font=(FONT_FAMILY_PRIMARY, 12, 'bold'))
        style.configure('Result.TLabel',
                        font=(FONT_FAMILY_DISPLAY, 56, 'bold'),  # Increased font size
                        foreground=ACCENT_COLOR)
        style.configure('TimeLeft.TLabel', font=(FONT_FAMILY_PRIMARY, 11, 'normal'))
        style.configure('Status.TLabel', font=(FONT_FAMILY_PRIMARY, 10, 'italic'))
        style.configure('CurrentTime.TLabel', font=(FONT_FAMILY_PRIMARY, 10, 'normal'))

        # --- Separator Style ---
        style.configure('HSeparator.TSeparator', background=BG_COLOR)

        # --- Entry Widget Style ---
        # Configure the default appearance of the Entry widget.
        style.configure('TEntry',
                        fieldbackground=ENTRY_BG,
                        foreground=ENTRY_FG,
                        insertcolor=ENTRY_FG,  # Cursor color
                        borderwidth=2,  # Set a border width
                        relief='flat',  # Make the border flat by default
                        padding=8,
                        bordercolor=CARD_COLOR)  # Set default border color to match the card

        # Define style changes for different widget states (e.g., focus, invalid).
        style.map('TEntry',
                  # Change the border color to the accent color when focused.
                  bordercolor=[('focus', ACCENT_COLOR), ('invalid', INVALID_BG)],
                  # Change the background color only when the input is invalid.
                  fieldbackground=[('invalid', INVALID_BG)],
                  # Make the border appear solid only when focused.
                  relief=[('focus', 'solid')])

    def _initialize_variables(self):
        """Initializes and traces all tkinter control variables."""
        # Using StringVar allows the UI to automatically update when the data changes.
        self.arrival_var = tk.StringVar(value="09:00")
        self.work_duration_var = tk.StringVar(value="8.0")
        self.lunch_break_var = tk.StringVar(value="30")

        # These variables are for display purposes.
        self.departure_time_var = tk.StringVar(value="--:--")
        self.time_left_var = tk.StringVar(value="")  # New variable for time remaining
        self.status_var = tk.StringVar(value="Enter your details.")
        self.current_time_var = tk.StringVar()

        # Tracing variables triggers a recalculation whenever their content changes.
        # The callback function will receive arguments, so we use *args to accept them.
        self.arrival_var.trace_add("write", self._recalculate_departure_time)
        self.work_duration_var.trace_add("write", self._recalculate_departure_time)
        self.lunch_break_var.trace_add("write", self._recalculate_departure_time)

    def _create_widgets(self):
        """Creates and places all the GUI widgets in a structured layout."""
        # Main frame with padding to give the app some breathing room.
        main_frame = ttk.Frame(self, padding=(20, 20, 20, 10))
        main_frame.pack(expand=True, fill=tk.BOTH)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Allow the output section to expand vertically.

        # --- Input Section ---
        input_card = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        input_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        input_card.columnconfigure(1, weight=1)

        # Input fields are laid out in a grid for easy alignment.
        # Set the background color of the labels to match the card.
        ttk.Label(input_card, text="Arrival Time (HH:MM)", background=CARD_COLOR).grid(row=0, column=0, sticky="w", pady=(0, 10))
        ttk.Entry(input_card, textvariable=self.arrival_var, justify='center').grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=(0, 10))

        ttk.Label(input_card, text="Work Duration (hours)", background=CARD_COLOR).grid(row=1, column=0, sticky="w", pady=(0, 10))
        ttk.Entry(input_card, textvariable=self.work_duration_var, justify='center').grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=(0, 10))

        ttk.Label(input_card, text="Lunch Break (minutes)", background=CARD_COLOR).grid(row=2, column=0, sticky="w")
        ttk.Entry(input_card, textvariable=self.lunch_break_var, justify='center').grid(row=2, column=1, sticky="ew", padx=(15, 0))

        # --- Output Section (Re-designed) ---
        output_card = ttk.Frame(main_frame, style='Card.TFrame', padding=(20, 25))
        output_card.grid(row=1, column=0, sticky="nsew")

        # Configure grid to center content. The rows with weight=1 act as spacers.
        output_card.rowconfigure(0, weight=1)
        output_card.rowconfigure(5, weight=1)
        output_card.columnconfigure(0, weight=1)

        # Set the background of labels within the card to match the card color.
        # All labels are placed in column 0 and will be centered by the column's weight.
        ttk.Label(output_card, text="ESTIMATED DEPARTURE", style='Header.TLabel', background=CARD_COLOR).grid(row=1, column=0)
        ttk.Label(output_card, textvariable=self.departure_time_var, style='Result.TLabel', background=CARD_COLOR).grid(row=2, column=0, pady=5)

        # Add a visual separator
        ttk.Separator(output_card, orient='horizontal', style='HSeparator.TSeparator').grid(row=3, column=0, sticky='ew', padx=20, pady=15)

        # New dedicated label for time remaining
        ttk.Label(output_card, textvariable=self.time_left_var, style='TimeLeft.TLabel', background=CARD_COLOR).grid(row=4, column=0)
        ttk.Label(output_card, textvariable=self.status_var, style='Status.TLabel', background=CARD_COLOR).grid(row=5, column=0, sticky='s', pady=(5, 0))

        # --- Footer ---
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        ttk.Label(footer_frame, textvariable=self.current_time_var, style='CurrentTime.TLabel').pack()

        # --- Add Focus Clearing Bindings ---
        # A list of widgets that should clear focus when clicked.
        # This includes frames and any non-interactive child widgets.
        widgets_to_bind = [
            main_frame, input_card, output_card, footer_frame,
            *input_card.winfo_children(),
            *output_card.winfo_children(),
            *footer_frame.winfo_children(),
        ]
        for widget in widgets_to_bind:
            # We only bind to non-entry widgets to avoid conflicts.
            if widget.winfo_class() != 'TEntry':
                widget.bind("<Button-1>", self._clear_focus)

    def _clear_focus(self, event):
        """Removes focus from the currently active widget by focusing the root window."""
        self.focus()

    def _recalculate_departure_time(self, *args):
        """
        Calculates the departure time based on user inputs.
        This method is robust against empty or invalid inputs.
        The *args parameter is required by the trace callback but is not used here.
        """
        try:
            # Retrieve values from the control variables.
            arrival_str = self.arrival_var.get()
            work_hours_str = self.work_duration_var.get()
            lunch_minutes_str = self.lunch_break_var.get()

            # Guard against empty fields to prevent errors during conversion.
            if not all([arrival_str, work_hours_str, lunch_minutes_str]):
                raise ValueError("An input field is empty.")

            # Convert string inputs to their appropriate numeric types.
            work_hours = float(work_hours_str)
            lunch_minutes = int(lunch_minutes_str)

            # Parse the arrival time string and combine it with today's date.
            now = datetime.datetime.now()
            arrival_time_obj = datetime.datetime.strptime(arrival_str, "%H:%M").time()
            arrival_datetime = now.replace(hour=arrival_time_obj.hour, minute=arrival_time_obj.minute, second=0, microsecond=0)

            # Calculate the departure time by adding durations to the arrival time.
            work_duration = datetime.timedelta(hours=work_hours)
            lunch_duration = datetime.timedelta(minutes=lunch_minutes)
            self.departure_datetime = arrival_datetime + work_duration + lunch_duration

            # Update the UI with the formatted result.
            self.departure_time_var.set(self.departure_datetime.strftime('%H:%M'))
            self._update_status_message()

        except (ValueError, TypeError):
            # This block catches various errors and resets the UI to a waiting state.
            self.departure_datetime = None
            self.departure_time_var.set("--:--")
            self.time_left_var.set("")  # Clear time left
            self.status_var.set("Waiting for valid input...")

    def _update_status_message(self):
        """Updates the time remaining and status message based on the current time."""
        if not self.departure_datetime:
            return  # Do nothing if we don't have a valid departure time.

        now = datetime.datetime.now()

        # To determine if the workday has started, we need the arrival time.
        # We recalculate it from the departure time to ensure consistency.
        try:
            work_duration = datetime.timedelta(hours=float(self.work_duration_var.get()))
            lunch_duration = datetime.timedelta(minutes=int(self.lunch_break_var.get()))
            arrival_datetime = self.departure_datetime - work_duration - lunch_duration
        except (ValueError, TypeError):
            # This handles cases where vars are changed to invalid values while the clock is running.
            self.status_var.set("Waiting for valid input...")
            self.time_left_var.set("")
            return

        # Compare the current time to the key moments of the day and update UI accordingly.
        if now < arrival_datetime:
            self.time_left_var.set("")
            self.status_var.set("Your workday has not started yet. ☀️")
        elif now >= self.departure_datetime:
            self.time_left_var.set("")
            self.status_var.set("Your workday is over. Time to go home! 🎉")
        else:
            # Calculate and display the remaining time.
            time_left = self.departure_datetime - now
            hours, remainder = divmod(time_left.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            self.time_left_var.set(f"Time Remaining: {int(hours)}h {int(minutes)}m")
            self.status_var.set("Work in progress... ⏳")

    def _update_clock(self):
        """Updates the current time display and status message every second."""
        self.current_time_var.set(datetime.datetime.now().strftime("Current Time: %H:%M:%S"))
        self._update_status_message()
        # Schedule this method to run again after 1000ms (1 second).
        self.after(1000, self._update_clock)

    def _load_settings(self):
        """Loads settings from the user's persistent file, falling back to the bundled default."""
        settings_path_to_load = PERSISTENT_SETTINGS_FILE

        if not os.path.exists(settings_path_to_load):
            settings_path_to_load = DEFAULT_SETTINGS_FILE

        try:
            with open(settings_path_to_load, 'r') as f:
                settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If all else fails, use hardcoded defaults
            settings = {
                "arrival": "09:00",
                "work_duration": "8.0",
                "lunch_break": "30"
            }

        self.arrival_var.set(settings.get("arrival", "09:00"))
        self.work_duration_var.set(settings.get("work_duration", "8.0"))
        self.lunch_break_var.set(settings.get("lunch_break", "30"))

    def _save_settings(self):
        """Saves the current input values to the persistent settings file."""
        settings = {
            "arrival": self.arrival_var.get(),
            "work_duration": self.work_duration_var.get(),
            "lunch_break": self.lunch_break_var.get()
        }
        # Save to the user's writable AppData folder
        with open(PERSISTENT_SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)

    def _on_closing(self):
        """Called when the application window is closed."""
        self._save_settings()  # Save the current values
        self.destroy()         # Close the application


if __name__ == "__main__":
    app = WorkTimerApp()
    app.mainloop()
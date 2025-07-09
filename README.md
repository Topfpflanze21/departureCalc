# Workday Departure Calculator

A simple yet effective Python script to calculate your work departure time based on your arrival, work duration, and lunch break. It also shows you the time remaining in your workday.

## Features

* **Modern Interface**: A clean and modern UI built with Python's native `tkinter` library.
* **Live Updates**: Displays the current time and a real-time countdown of your remaining workday.
* **Smart Status**: The status message updates based on the time of day ("Work in progress... ⏳", "Time to go home! 🎉").
* **Persistent Settings**: Automatically saves your last-used arrival time, work duration, and lunch break for convenience.
* **Easy Configuration**: Colors and fonts can be easily customized by changing the constants at the top of the script.
* **No Dependencies**: Runs out-of-the-box with a standard Python 3 installation.

---

## Requirements

* **Python 3.x**

That's it! All necessary libraries (`tkinter`, `datetime`, `json`) are included with Python.

---

## How to Use

1.  **Create a `data` folder** in the same directory where you save the Python script. The application will use this folder to store your settings.
    ```
    /your_project_folder/
    |-- workday_calculator.py  (your script)
    |-- /data/                  (create this folder)
    ```
2.  **Run the script** from your terminal:
    ```bash
    python workday_calculator.py
    ```
3.  **Enter your details**:
    * **Arrival Time**: The time you started work (in 24-hour HH:MM format).
    * **Work Duration**: Your total workday length in hours (e.g., `8.0`).
    * **Lunch Break**: Your lunch break duration in minutes (e.g., `30`).

The departure time and time remaining will update automatically. Your inputs will be saved when you close the application.

---

## Configuration

You can customize the application's appearance by modifying the constants at the top of the script file.

* **Colors**: Change `BG_COLOR`, `FG_COLOR`, `CARD_COLOR`, `ACCENT_COLOR`, etc., to alter the theme.
* **Fonts**: Modify `FONT_FAMILY_PRIMARY` and `FONT_FAMILY_DISPLAY` to change the typography.
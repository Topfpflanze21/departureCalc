# Workday Departure Calculator

A simple yet effective Python script to calculate your work departure time based on your arrival, work duration, and lunch break. It also shows you the time remaining in your workday.

## Installation (Recommended)

1.  Go to the [**Releases**](https://github.com/Topfpflanze21/departureCalc/releases) page.
2.  From the latest release, download the setup `.exe` file from the **Assets** section.
3.  Run the installer and launch the application from the Start Menu or desktop shortcut.

## Features

* **Modern Interface**: A clean and modern UI built with Python's native `tkinter` library.
* **Live Updates**: Displays the current time and a real-time countdown of your remaining workday.
* **Smart Status**: The status message updates based on the time of day ("Work in progress... ⏳", "Time to go home! 🎉").
* **Persistent Settings**: Automatically saves your last-used arrival time, work duration, and lunch break for convenience.
* **Easy Configuration**: Colors and fonts can be easily customized by changing the constants at the top of the script.
* **No Dependencies**: Runs out-of-the-box with a standard Python 3 installation.

---

## Running from Source (For Developers)

### Requirements

* **Python 3.x**

That's it! All necessary libraries (`tkinter`, `datetime`, `json`) are included with Python.

### How to Use

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd departureCalc
    ```
2.  **Run the script** from your terminal:
    ```bash
    python main.py
    ```

---

## Configuration

You can customize the application's appearance by modifying the constants at the top of the `main.py` script file.

* **Colors**: Change `BG_COLOR`, `FG_COLOR`, `CARD_COLOR`, `ACCENT_COLOR`, etc., to alter the theme.
* **Fonts**: Modify `FONT_FAMILY_PRIMARY` and `FONT_FAMILY_DISPLAY` to change the typography.
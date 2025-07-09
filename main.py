import datetime

# --- CONFIGURE YOUR TIMES HERE ---
ARRIVAL_TIME_STR = "07:45"
WORK_DURATION_HOURS = 8
LUNCH_BREAK_MINUTES = 30

def calculate_departure(arrival_dt, work_hours, lunch_minutes):
    """
    Calculates the departure time by adding work and lunch durations to the arrival time.
    """
    work_duration = datetime.timedelta(hours=work_hours)
    lunch_duration = datetime.timedelta(minutes=lunch_minutes)
    return arrival_dt + work_duration + lunch_duration

def display_status(now, arrival_dt, departure_dt):
    """
    Prints the current work status based on the current time.
    """
    print("-" * 25)
    if now < arrival_dt:
        print("Your workday has not started yet. ☀️")
    elif now >= departure_dt:
        print("Your workday is over. Time to go home! 🎉")
    else:
        time_left = departure_dt - now
        hours, remainder = divmod(time_left.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"Current Time:         {now.strftime('%H:%M')}")
        print(f"Time Remaining:       {int(hours)}h {int(minutes)}m ⏳")

def main():
    """
    Main function to run the work time calculator.
    """
    try:
        # Get current time and parse arrival time from configuration
        now = datetime.datetime.now()
        arrival_time_obj = datetime.datetime.strptime(ARRIVAL_TIME_STR, "%H:%M").time()
        arrival_datetime = now.replace(hour=arrival_time_obj.hour, minute=arrival_time_obj.minute, second=0, microsecond=0)

        # Calculate the departure time
        leaving_datetime = calculate_departure(arrival_datetime, WORK_DURATION_HOURS, LUNCH_BREAK_MINUTES)

        # --- Display Information ---
        print(f"Arrival Time:         {arrival_datetime.strftime('%H:%M')}")
        print(f"Work Duration:        {WORK_DURATION_HOURS} hours")
        print(f"Lunch Break:          {LUNCH_BREAK_MINUTES} minutes")
        print("-" * 25)
        print(f"Calculated Departure: {leaving_datetime.strftime('%H:%M')}")

        # Display the current status based on the calculated times
        display_status(now, arrival_datetime, leaving_datetime)

    except ValueError:
        print("Error: Please check the ARRIVAL_TIME_STR format. It should be HH:MM (e.g., '09:00').")

# --- SCRIPT EXECUTION ---
if __name__ == "__main__":
    main()
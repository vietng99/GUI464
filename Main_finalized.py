import tkinter as tk
from tkinter import ttk
import datetime
import time
import serial
import serial.tools.list_ports
import threading
import sys
import warnings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import ctypes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from tkinter import messagebox

##################################################################################################################################
ser = None
ax = None
canvas = None
##################################################################################################################################

def update_plot():
    global ax, canvas

    if not ax or not canvas:
        return

    # Clear the current plot
    ax.clear()
    t, y = generate_waveform()
    ax.plot(t, y)
    ax.set_title('Pulse Chain Visualization')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    canvas.draw()

# Configuration storage
config_storage = {
    "frequency": None,
    "duty_cycle": None,
    "pulse_chain": []
}

def update_frequency(value):
    global ser  # Ensure ser is accessible globally
    config_storage["frequency"] = int(value)
    info_frequency_label.config(text=f"Frequency: {value} Hz")
    update_data_log("Frequency Updated", freq=value, duty_cycle=config_storage.get('duty_cycle', 'N/A'))
    root.update_idletasks()
    command = f"FREQ:{value}\n"
    # Check if ser is not None and the port is open before writing
    if ser is not None and ser.is_open:
        ser.write(command.encode())
    else:
        print("Serial port is not open.")
    update_plot()
    refresh_window()
    refresh_window()

def update_duty_cycle(value):
    global ser  # Ensure ser is accessible globally
    config_storage["duty_cycle"] = int(value)
    info_duty_cycle_label.config(text=f"Duty Cycle: {value}%")
    update_data_log("Duty Cycle Updated", freq=config_storage.get('frequency', 'N/A'), duty_cycle=value)
    root.update_idletasks()
    command = f"DUTY:{value}\n"
    # Check if ser is not None and the port is open before writing
    if ser is not None and ser.is_open:
        ser.write(command.encode())
    else:
        print("Serial port is not open.")
    update_plot()
    refresh_window()
    refresh_window()

def timer_countdown():
    global timer_seconds
    while timer_seconds > 0:
        time.sleep(1)  # Wait for a second
        timer_seconds -= 1  # Decrement the timer

        # Convert seconds to HH:MM:SS:MS for display
        hours, minutes = divmod(timer_seconds, 3600)
        minutes, seconds = divmod(minutes, 60)
        milliseconds = 0  # Still no milliseconds; keep as 0
        update_timer_display(h=hours, m=minutes, s=seconds, ms=milliseconds)

        if timer_seconds <= 0:
            # Automatically stop and reset the timer when it runs out
            stop_command()
            reset_command()
            reset_timer_display()  # Reset the timer display to 00:00:00.000
            start_command()

def refresh_window():
    refresh_info_bar()
    root.update_idletasks()
    root.update()
    display_pulse_chain()

def refresh_info_bar():
    # Assuming current_com_port and current_baud_rate are updated elsewhere in your application
    global current_com_port, current_baud_rate

    # Update the info bar labels with the latest values from config_storage or other state variables
    info_frequency_label.config(text=f"Frequency: {config_storage.get('frequency', '--')} Hz")
    info_duty_cycle_label.config(text=f"Duration: {config_storage.get('duty_cycle', '--')}%")
    info_current_runtime_label.config(text=f"Current Runtime: {config_storage.get('current_runtime', '--')}")
    info_expected_runtime_label.config(text=f"Expected Runtime: {config_storage.get('expected_runtime', '--')}")
    #info_preset_name_label.config(text=f"Preset: {config_storage.get('preset_name', 'None')}")

    # Update COM Port and Baud Rate labels
    if ser is not None and ser.is_open:
        current_com_port = ser.port
        current_baud_rate = ser.baudrate
        info_com_port_label.config(text=f"COM Port: {current_com_port}")
        info_baud_rate_label.config(text=f"Baud Rate: {current_baud_rate}")
    else:
        info_com_port_label.config(text="COM Port: N/A")
        info_baud_rate_label.config(text="Baud Rate: --")

    # Force a refresh of the entire GUI to reflect these updates
    root.update_idletasks()

def get_border_color(original_color):
    return original_color if border_visible else 'white'

def update_clock():
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Format time with milliseconds
    real_time_clock.config(text=now)
    real_time_clock.after(10, update_clock)

# Stopwatch state variables
stopwatch_running = False
start_time = None
elapsed_time = 0
def update_stopwatch_display():
    if stopwatch_running:
        # Calculate elapsed time
        current_time = time.time()
        total_elapsed = elapsed_time + (current_time - start_time)
        # Format the time as H:M:S.ms
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(total_elapsed)) + f'.{str(int(total_elapsed * 1000) % 1000).zfill(3)}'
        stopwatch_display.config(text=f"Stopwatch: {formatted_time}")
        # Schedule the next update
        root.after(10, update_stopwatch_display)

def update_data_log(action, freq='N/A', duty_cycle='N/A'):
    # Get current time and format it
    now = datetime.datetime.now()
    date_str = now.strftime('%y/%m/%d')
    time_str = now.strftime('%H:%M:%S')
    stopwatch_time = int(elapsed_time * 1000)  # Assuming elapsed_time is available globally

    # Insert each part with its color tag
    data_log_window.config(state=tk.NORMAL)
    data_log_window.insert(tk.END, f"{date_str} ", "date")
    data_log_window.insert(tk.END, f"{time_str}: ", "timestamp")
    data_log_window.insert(tk.END, f"{stopwatch_time}ms: ", "stopwatch")
    data_log_window.insert(tk.END, f"{action}: \n", "action")
    # Indent for info part, adjust spaces as needed for alignment
    indent = ' ' * 20
    data_log_window.insert(tk.END, f"{indent}Frequency=", "action")
    data_log_window.insert(tk.END, f"{freq}Hz, ", "frequency")
    data_log_window.insert(tk.END, "Duration=", "action")
    data_log_window.insert(tk.END, f"{duty_cycle}%\n", "duty_cycle")
    data_log_window.config(state=tk.DISABLED)

    # Ensure the scrollbar moves down to show the latest entry
    data_log_window.see(tk.END)
    # Define color tags
    color_tags = {
        "date": ("hot pink",),
        "timestamp": ("red",),
        "stopwatch": ("green",),
        "action": ("black",),
        "frequency": ("purple",),
        "duty_cycle": ("blue",)
    }

    for tag, (color,) in color_tags.items():
        data_log_window.tag_configure(tag, foreground=color)
    root.update_idletasks()

def start_command():
    global ser, stopwatch_running, start_time, elapsed_time, timer_seconds

    if not stopwatch_running:
        stopwatch_running = True
        start_time = time.time()
        update_stopwatch_display()

    # Log the start action
    freq = config_storage.get('frequency', 'N/A')
    duty_cycle = config_storage.get('duty_cycle', 'N/A')
    update_data_log('start', freq, duty_cycle)

    # Start the timer countdown in a separate thread to avoid blocking the GUI
    if timer_seconds > 0:  # Ensure there's a timer set
        countdown_thread = threading.Thread(target=timer_countdown)
        countdown_thread.start()

    # Improved data sending functionality
    if ser is not None and ser.is_open:
        try:
            pulse_chain_list = config_storage.get("pulse_chain", [])
            pulse_chain_str = ','.join(map(str, pulse_chain_list))
            sequence_size = len(pulse_chain_list)
            frequency = config_storage.get("frequency", 0)
            duty_cycle = config_storage.get("duty_cycle", 0)
            data_str = f"<{sequence_size},{frequency},{duty_cycle},{pulse_chain_str}>"
            print(f"Sending to device: {data_str}")
            ser.write(data_str.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error during send: {e}")
            print(f"Details: {e.args}")

    else:
        print("Serial port is not open. Attempting to reconnect...")
        selected_com_port = auto_connect()
        if selected_com_port:
            try:
                ser = serial.Serial(selected_com_port, 9600, timeout=1)
                print("Reconnection successful.")
            except serial.SerialException as e:
                print(f"Failed to reconnect: {e}")
                print(f"Details: {e.args}")
        else:
            print("No available COM ports found for reconnection.")



def stop_command():
    global ser, stopwatch_running, elapsed_time, start_time, timer_seconds
    if stopwatch_running:
        elapsed_time += time.time() - start_time
        stopwatch_running = False
        start_time = None

    # Stop the timer countdown
    timer_seconds = 0  # Ensures the countdown loop exits

    config_storage["frequency"] = None
    config_storage["duty_cycle"] = None

    # Existing functionality to send the stop signal to the device
    if ser is not None and ser.is_open:
        try:
            pulse_chain_list = config_storage.get("pulse_chain", [])
            pulse_chain_str = ','.join(map(str, pulse_chain_list))
            sequence_size = len(pulse_chain_list)
            frequency = config_storage.get("frequency", 0)
            duty_cycle = config_storage.get("duty_cycle", 0)
            data_str = f"<{sequence_size},{frequency},{duty_cycle},{pulse_chain_str}>"
            print(f"Sending to device: {data_str}")
            ser.write(data_str.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error during send: {e}")
            print(f"Details: {e.args}")

    else:
        print("Serial port is not open. Attempting to reconnect...")
        selected_com_port = auto_connect()
        if selected_com_port:
            try:
                ser = serial.Serial(selected_com_port, 9600, timeout=1)
                print("Reconnection successful.")
            except serial.SerialException as e:
                print(f"Failed to reconnect: {e}")
                print(f"Details: {e.args}")
        else:
            print("No available COM ports found for reconnection.")


    # Log the stop action
    freq = config_storage.get('frequency', 'N/A')
    duty_cycle = config_storage.get('duty_cycle', 'N/A')
    update_data_log('stop', freq, duty_cycle)


def reset_command():
    global ser, elapsed_time, start_time, stopwatch_running, timer_seconds
    elapsed_time = 0
    stopwatch_running = False
    start_time = None
    timer_seconds = 0  # Reset the timer duration

    config_storage["frequency"] = None
    config_storage["duty_cycle"] = None

    # Existing functionality to send the reset signal to the device
    if ser is not None and ser.is_open:
        try:
            pulse_chain_list = config_storage.get("pulse_chain", [])
            pulse_chain_str = ','.join(map(str, pulse_chain_list))
            sequence_size = len(pulse_chain_list)
            frequency = config_storage.get("frequency", 0)
            duty_cycle = config_storage.get("duty_cycle", 0)
            data_str = f"<{sequence_size},{frequency},{duty_cycle},{pulse_chain_str}>"
            print(f"Sending to device: {data_str}")
            ser.write(data_str.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error during send: {e}")
            print(f"Details: {e.args}")

    else:
        print("Serial port is not open. Attempting to reconnect...")
        selected_com_port = auto_connect()
        if selected_com_port:
            try:
                ser = serial.Serial(selected_com_port, 9600, timeout=1)
                print("Reconnection successful.")
            except serial.SerialException as e:
                print(f"Failed to reconnect: {e}")
                print(f"Details: {e.args}")
        else:
            print("No available COM ports found for reconnection.")

    update_stopwatch_display()
    stopwatch_display.config(text="Stopwatch: 00:00:00.000")
    update_timer_display()  # Reset the timer display to 00:00:00:000

    # Reset actions for frequency and duty cycle

    frequency_scale.set(1700)  # Reset slider to a neutral position
    duty_cycle_scale.set(30)  # Reset slider to a neutral position
    frequency_entry.delete(0, tk.END)  # Clear the entry box
    duty_cycle_entry.delete(0, tk.END)  # Clear the entry box
    info_frequency_label.config(text="Frequency: -- Hz")
    info_duty_cycle_label.config(text="Duration: --ms")
    update_data_log("Reset", freq="N/A", duty_cycle="N/A")

    root.update_idletasks()
    refresh_window()



def open_pulse_chain_config():
    new_window = tk.Toplevel()
    new_window.title("Pulse Chain Configuration")
    new_window.geometry("600x400")

    canvas = tk.Canvas(new_window, borderwidth=0)
    scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    rows = []  # List to keep track of row widgets

    def add_row():
        row_number = len(rows)
        entry = tk.Entry(scrollable_frame, width=25)
        entry.grid(row=row_number, column=1, padx=10, pady=10)

        toggle_text = "On" if row_number % 2 == 0 else "Off"
        toggle_bg = "green" if row_number % 2 == 0 else "red"
        switch_var = tk.BooleanVar(value=(row_number % 2 == 0))
        toggle = tk.Checkbutton(scrollable_frame, text=toggle_text, bg=toggle_bg, variable=switch_var, state="disabled")
        toggle.grid(row=row_number, column=2, padx=10, pady=10)

        rows.append({"entry": entry, "toggle": toggle})

    def delete_last_row():
        if rows:
            last_row = rows.pop()
            last_row['entry'].destroy()
            last_row['toggle'].destroy()

    def close_window():
        pulse_chain_values = []
        for row in rows:
            entry_value = row['entry'].get()
            try:
                value = int(float(entry_value) * 1000)
                pulse_chain_values.append(value)
            except ValueError:
                print(f"Ignoring non-numeric input: {entry_value}")

        config_storage["pulse_chain"] = pulse_chain_values
        print("Pulse Chain Config:", config_storage["pulse_chain"])
        new_window.destroy()

    add_row_button = tk.Button(scrollable_frame, text="+", command=add_row, width=3, height=2)
    add_row_button.grid(row=0, column=3, padx=10, pady=10)

    delete_row_button = tk.Button(scrollable_frame, text="-", command=delete_last_row, width=3, height=2)
    delete_row_button.grid(row=0, column=4, padx=10, pady=10)

    add_row()  # Add the first row automatically

    confirm_button = tk.Button(new_window, text="Confirm", command=close_window)
    confirm_button.pack(pady=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    display_pulse_chain()
    refresh_window()
    refresh_window()

    def on_close():
        display_pulse_chain()
        refresh_window()
        refresh_window()

        new_window.destroy()

    new_window.protocol("WM_DELETE_WINDOW", on_close)

last_known_pulse_chain = []

def check_pulse_chain_update():
    global last_known_pulse_chain

    if config_storage["pulse_chain"] != last_known_pulse_chain:
        display_pulse_chain()
        last_known_pulse_chain = config_storage["pulse_chain"].copy()


    root.after(1000, check_pulse_chain_update)


def update_pulse_chain_config(new_config_str):


    # Split the new_config_str by commas to get a list of durations
    durations = new_config_str.split(", ")


    formatted_config = '\n'.join([
        f"{durations[i]} {'on' if i % 2 == 0 else 'off'}" for i in range(len(durations))
    ])



def display_pulse_chain():
    pulse_chain_display.config(state=tk.NORMAL)
    pulse_chain_display.delete(1.0, tk.END)

    pulse_chain = config_storage["pulse_chain"]

    if not pulse_chain:
        pulse_chain_display.insert(tk.END, "N/A")
    else:

        pulse_chain_display.tag_configure('on_tag', foreground='green')
        pulse_chain_display.tag_configure('off_tag', foreground='red')


        for i, value in enumerate(pulse_chain):
            state = 'on' if i % 2 == 0 else 'off'
            tag = 'on_tag' if state == 'on' else 'off_tag'
            formatted_value = f"{value/1000} ms {state} \n"
            pulse_chain_display.insert(tk.END, formatted_value, tag)

    pulse_chain_display.config(state=tk.DISABLED)



def validate_entry_input(P):
    if P.replace('.', '', 1).isdigit() or P == "":
        return True
    return False


def update_entry_from_slider(slider, entry):
    entry.delete(0, tk.END)
    entry.insert(0, str(slider.get()))

def update_slider_from_entry(entry, slider):
    try:
        slider.set(float(entry.get()))
    except ValueError:
        pass



def auto_connect():
    try:
        ports = [p.device for p in serial.tools.list_ports.comports()]
        if not ports:
            raise IOError("No compatible device found - available ports: {}".format(ports))
        serialPort = ports[1]
        baudRate = 9600
        global ser
        ser = serial.Serial(serialPort, baudRate)
        time.sleep(2)  # Delay to ensure the connection is ready
        print(f"Device connected on {serialPort} at {baudRate} bps")
        # Update the info bar with the connection details
        info_com_port_label.config(text=f"COM Port: {serialPort}")
        info_baud_rate_label.config(text=f"Baud Rate: {baudRate}")
    except Exception as e:
        print(f"Error: {e}")
        info_com_port_label.config(text="COM Port: Connection Failed")
        info_baud_rate_label.config(text="Baud Rate: --")


    # try:
    #     ports = list(serial.tools.list_ports.comports())
    #     teensy_port = None
    #     for port in ports:
    #         if "Teensy" in port.description:  # Adjust the identifier as needed
    #             teensy_port = port.device
    #             break
    #
    #     if teensy_port is None:
    #         raise IOError("No Teensy 4.1 found - available ports: {}".format([p.device for p in ports]))
    #
    #     baudRate = 9600
    #     global ser
    #     ser = serial.Serial(teensy_port, baudRate)
    #     time.sleep(2)
    #     print(f"Device connected on {teensy_port} at {baudRate} bps")
    #
    #     info_com_port_label.config(text=f"COM Port: {teensy_port}")
    #     info_baud_rate_label.config(text=f"Baud Rate: {baudRate}")
    # except Exception as e:
    #     print(f"Error: {e}")
    #     info_com_port_label.config(text="COM Port: Connection Failed")
    #     info_baud_rate_label.config(text="Baud Rate: --")


def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help")
    help_window.geometry("1200x900")  # Adjust the size as needed

    # Create a Text widget for displaying the help content
    help_text = tk.Text(help_window, wrap="word", bg="white")
    help_text.pack(expand=True, fill="both", padx=10, pady=10)

    # Define tags for styling
    help_text.tag_configure("title", foreground="blue", underline=True, font=('Helvetica', '16', 'bold underline'))
    help_text.tag_configure("subtitle", foreground="hot pink", font=('Helvetica', '14', 'bold'))
    help_text.tag_configure("special_note", foreground="red", font=('Helvetica', '12', 'italic'))
    help_text.tag_configure("update_bug", foreground="purple", font=('Helvetica', '12', 'italic'))
    help_text.tag_configure("normal", font=('Helvetica', '12'))

    # Inserting the formatted content
    help_text.insert("end", "Help Window Content (Updated)\n", "title")
    help_text.insert("end", "\nDisplay Overview:\n", "subtitle")
    help_text.insert("end",
                     "Currently, the display area is inactive as we await integration with the Picoscope. Future updates might include displaying theoretical data based on settings, though this is not a current priority.\n",
                     "normal")

    help_text.insert("end", "\nInfo Bar Details:\n", "subtitle")
    help_text.insert("end",
                     "Located directly below the display, the info bar presents crucial settings and timings: frequency, duty cycle, current runtime, expected runtime, preset name, COM port, and Baud rate. Frequency and duty cycle values are derived from settings, current runtime from the stopwatch, expected runtime from pulse chain configuration, and preset name from the load preset function. The preset feature is under development, so no information is displayed here yet.\n",
                     "normal")

    help_text.insert("end", "\nStopwatch and Clock:\n", "subtitle")
    help_text.insert("end",
                     "The stopwatch measures time to a precision of 10ms. Alongside, a real-time clock provides additional timekeeping. Both serve as timestamps for future log entries.\n",
                     "normal")
    help_text.insert("end",
                     "Warning: There is currently a bug that affects the stopwatch functionality. Starting, stopping, and then starting again does not resume from the previous stop value but instead doubles every time. We are actively working to resolve this issue.\n",
                     "update_bug")

    help_text.insert("end", "\nLog Window (Update):\n", "subtitle")
    help_text.insert("end",
                     "The log feature is now fully implemented and functional. It supports color coding for various components such as the year, date, day, real-time, time from the stopwatch, action, and info such as frequency and duty cycle, making it easier to distinguish between different types of log entries.\n",
                     "normal")

    help_text.insert("end", "\nData and Settings (Update):\n", "subtitle")
    help_text.insert("end",
                     "The settings window now enables users to pick their COM port as well as baud rate and timeout dynamically. It automatically detects all available ports from the system. Note: There is still a bug where trying to connect to a port that cannot be used causes the app to freeze. This issue is currently being addressed.\n",
                     "normal")

    help_text.insert("end", "\nHelp Functionality:\n", "subtitle")
    help_text.insert("end",
                     "You're looking at it! This note aims to clarify current functionalities and known issues.\n",
                     "special_note")

    help_text.insert("end", "\nRefresh Mechanism:\n", "subtitle")
    help_text.insert("end",
                     "The refresh button is designed to redraw the application interface. An anomaly requires a double click for effectiveness. This workaround is temporary.\n",
                     "normal")

    help_text.insert("end", "\nConnectivity Controls:\n", "subtitle")
    help_text.insert("end",
                     "Connect and disconnect buttons are straightforward: they manage the connection between the Arduino and the PC.\n",
                     "normal")

    # Disable editing of the text widget
    help_text.config(state="disabled")

    # Optionally, add a scrollbar to the Text widget
    scrollbar = tk.Scrollbar(help_window, command=help_text.yview)
    scrollbar.pack(side="right", fill="y")
    help_text.config(yscrollcommand=scrollbar.set)







def update_frequency_entry(value):
    frequency_entry.delete(0, tk.END)
    frequency_entry.insert(0, str(value))

def on_frequency_entry_change(event=None):
    try:
        # Get the value from the entry box and update the slider and config
        value = float(frequency_entry.get())
        frequency_scale.set(value)
        update_frequency(value)
    except ValueError:
        # Handle the case where the entry box does not contain a valid number
        pass


def update_duty_cycle_entry(value):
    duty_cycle_entry.delete(0, tk.END)
    duty_cycle_entry.insert(0, str(value))

def on_duty_cycle_entry_change(event=None):
    try:
        # Get the value from the entry box and update the slider and config
        value = float(duty_cycle_entry.get())
        duty_cycle_scale.set(value)
        update_duty_cycle(value)
    except ValueError:
        # If the entry does not contain a valid number, do nothing or reset to previous value
        pass


timer_seconds = 0  # Global variable to keep track of the timer duration in seconds


def confirm_timer():
    global timer_seconds
    timer_seconds = int(timer_entry.get())  # Retrieve and store the timer duration

    # Convert seconds to HH:MM:SS:MS
    hours, minutes = divmod(timer_seconds, 3600)
    minutes, seconds = divmod(minutes, 60)
    milliseconds = 0  # No milliseconds input; set to 0

    # Update the timer display
    update_timer_display(h=hours, m=minutes, s=seconds, ms=milliseconds)

def reset_timer_display():
    # Reset the timer display to 00:00:00:000
    update_timer_display()

def generate_wavef():
    frequency = float(config_storage.get("frequency", 0))
    duty_cycle = float(config_storage.get("duty_cycle", 0)) / 100
    sequence = config_storage.get("pulse_chain", [])
    sequence = [x / 1000 for x in sequence]
    print(sequence)

    t = [0]
    y = [0]
    current_time = 0

    for i, duration_ms in enumerate(sequence):
        duration_s = duration_ms / 1000
        if i % 2 == 0:
            total_cycles = int(frequency * duration_s)
            cycle_duration = 1 / frequency
            high_duration = cycle_duration * duty_cycle
            low_duration = cycle_duration - high_duration

            for _ in range(total_cycles):
                t.append(current_time)
                y.append(1)
                current_time += high_duration
                t.append(current_time)
                y.append(1)
                
                t.append(current_time)
                y.append(0)
                current_time += low_duration
                t.append(current_time)
                y.append(0)

        else:
            t.append(current_time)
            y.append(0)
            current_time += duration_s
            t.append(current_time)
            y.append(0)

    return t, y

def open_preview_display():
    preview_window = tk.Toplevel(root)
    preview_window.title("Preview Display")
    window_width = 800
    window_height = 800
    preview_window.geometry(f"{window_width}x{window_height}")

    main_x, main_y, main_width = root.winfo_x(), root.winfo_y(), root.winfo_width()
    gap = 20
    new_x, new_y = main_x + main_width + gap, main_y
    preview_window.geometry(f"+{new_x}+{new_y}")
    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)
    t, y = generate_wavef()

    #for time, amplitude in zip(t, y):
    #    print(f"Time: {time}, Amplitude: {amplitude}")

    ax.step(t, y, where='post')
    ax.plot(t, y)
    ax.set_title('Pulse Chain Visualization')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(figure, master=preview_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, preview_window)
    toolbar.update()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()
    canvas.flush_events()

def generate_waveform():
    # Example waveform data generation
    # Replace this logic with your actual frequency, duration, and pulse chain calculations
    t = np.linspace(0, 1, 1000)  # Time axis
    y = np.sin(2 * np.pi * 5 * t)  # Example sine wave with frequency of 5 Hz
    return t, y




# Flag to control border visibility
border_visible = False  # Set to False for invisible borders, True for visible

# Initialize the main window
root = tk.Tk()
root.title('GUI')
root.geometry('1200x800')
root.after(5, start_command)
root.after(10, refresh_window)
root.after(1000, check_pulse_chain_update)

# Create frames with adjustable border color
validate_command = (root.register(validate_entry_input), '%P')

display_frame = tk.Frame(root, height=320, width=800, bg='white',
                         highlightbackground=get_border_color('red'),
                         highlightthickness=2)
display_frame.place(x=0, y=0, anchor='nw')
display_frame.pack_propagate(False)

time_frame = tk.Frame(root, height=400, width=380, bg='white',
                      highlightbackground=get_border_color('blue'),
                      highlightthickness=2)
time_frame.place(x=1200, y=0, anchor='ne')
time_frame.pack_propagate(False)

config_frame = tk.Frame(root, height=470, width=600, bg='white',
                        highlightbackground=get_border_color('green'),
                        highlightthickness=2)
config_frame.place(x=0, y=330, anchor='nw')
config_frame.pack_propagate(False)

util_frame = tk.Frame(root, height=300, width=380, bg='white',
                      highlightbackground=get_border_color('orange'),
                      highlightthickness=2)
util_frame.place(x=1200, y=800, anchor='se')
util_frame.pack_propagate(False)

#Red Frame
dynamic_display = tk.Canvas(display_frame, bg='lightgrey', height=280, width=800, highlightbackground='black', highlightthickness=1)
dynamic_display.pack()

# Define a function to update the display with the timer
def update_timer_display(h=0, m=0, s=0, ms=0):
    # Format the time as HH:MM:SS.ms
    time_str = f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    # Coordinates for the timer and labels
    timer_x, timer_y = 400, 100  # Adjust as needed for your layout
    label_offset_y = 70  # Offset for the labels below the timer

    # Check if the timer display exists, if not, create it along with labels
    if 'timer_display' not in globals():
        global timer_display, hours_label, minutes_label, seconds_label, milliseconds_label
        timer_display = dynamic_display.create_text(timer_x, timer_y, text=time_str, font=('Helvetica', 48), fill="black")

        # Create labels for Hours, Minutes, Seconds, MS
        hours_label = dynamic_display.create_text(timer_x - 150, timer_y + label_offset_y, text="Hours", font=('Helvetica', 16), fill="black")
        minutes_label = dynamic_display.create_text(timer_x - 65, timer_y + label_offset_y, text="Minutes", font=('Helvetica', 16), fill="black")
        seconds_label = dynamic_display.create_text(timer_x + 40, timer_y + label_offset_y, text="Seconds", font=('Helvetica', 16), fill="black")
        milliseconds_label = dynamic_display.create_text(timer_x + 165, timer_y + label_offset_y, text="Milliseconds", font=('Helvetica', 16), fill="black")
    else:
        # Update the existing timer display
        dynamic_display.itemconfig(timer_display, text=time_str)

# Initialize the timer display and labels
update_timer_display()



# Add an information bar below the dynamic display
info_bar = tk.Label(display_frame, bg='white', height=30, width=800, highlightbackground='black', highlightthickness=1)
info_bar.pack(side='bottom', fill='x')

info_frequency_label = tk.Label(info_bar, text="Frequency: --", bg='white')
info_duty_cycle_label = tk.Label(info_bar, text="Duration: --", bg='white')
info_current_runtime_label = tk.Label(info_bar, text="Current Runtime: --", bg='white')
info_expected_runtime_label = tk.Label(info_bar, text="Expected Runtime: --", bg='white')
#info_preset_name_label = tk.Label(info_bar, text="Preset: None", bg='white')
info_com_port_label = tk.Label(info_bar, text="COM Port: N/A", bg='white')
info_baud_rate_label = tk.Label(info_bar, text="Baud Rate: --", bg='white')

#timer
timer_label = tk.Label(config_frame, text="Timer (s)")
timer_label.place(x=10, y=160)  # Adjust positioning as needed
timer_unit_label = tk.Label(config_frame, text="seconds", bg='white')
timer_unit_label.place(x=250, y=160)
timer_entry = tk.Entry(config_frame, width=15, validate='key', validatecommand=validate_command)
timer_entry.place(x=150, y=160)

confirm_timer_button = tk.Button(config_frame, text="Set Timer", command=confirm_timer)
confirm_timer_button.place(x=300, y=160)  # Adjust positioning as needed

# Packing the labels into the info bar
info_frequency_label.pack(side='left', padx=10)
info_duty_cycle_label.pack(side='left', padx=10)
info_current_runtime_label.pack(side='left', padx=10)
info_expected_runtime_label.pack(side='left', padx=10)
#info_preset_name_label.pack(side='left', padx=10)
info_com_port_label.pack(side='left', padx=10)
info_baud_rate_label.pack(side='left', padx=10)

#Green Frame
start_button = tk.Button(config_frame, text="Start", command=start_command, width=10, height=2)
start_button.place(x=10, y=10)

stop_button = tk.Button(config_frame, text="Stop", command=stop_command, width=10, height=2)
stop_button.place(x=110, y=10)

reset_button = tk.Button(config_frame, text="Reset", command=reset_command, width=10, height=2)
reset_button.place(x=220, y=10)

# Add the Preview Display Button in the config_frame
preview_display_button = tk.Button(config_frame, text="Preview Display", command=open_preview_display, width=12, height=2)
preview_display_button.place(x=500, y=10)  # Adjust the x-coordinate as necessary to position next to the reset button


# Frequency Adjustment UI Components
frequency_label = tk.Label(config_frame, text="Frequency Adjustment")
frequency_label.place(x=10, y=60)

frequency_scale = tk.Scale(config_frame, from_=50, to=10000, orient='horizontal', length=200)
frequency_scale.place(x=150, y=60)
frequency_scale.bind('<ButtonRelease-1>', lambda event: [update_frequency(frequency_scale.get()), update_frequency_entry(frequency_scale.get())])

frequency_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
frequency_entry.place(x=360, y=60)
frequency_entry.bind("<Return>", lambda event: update_slider_from_entry(frequency_entry, frequency_scale) or update_frequency(frequency_entry.get()))

frequency_unit_label = tk.Label(config_frame, text="Hz")
frequency_unit_label.place(x=400, y=60)

frequency_entry.bind("<Return>", on_frequency_entry_change)
frequency_entry.bind("<FocusOut>", on_frequency_entry_change)

# Duty Cycle Control UI Components
duty_cycle_label = tk.Label(config_frame, text="Duration Per Pulse")
duty_cycle_label.place(x=10, y=110)

duty_cycle_scale = tk.Scale(config_frame, from_=0, to=100, orient='horizontal', length=200)
duty_cycle_scale.place(x=150, y=110)
duty_cycle_scale.bind('<ButtonRelease-1>', lambda event: [update_duty_cycle(duty_cycle_scale.get()), update_duty_cycle_entry(duty_cycle_scale.get())])


duty_cycle_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
duty_cycle_entry.place(x=360, y=110)
duty_cycle_entry.bind("<Return>", lambda event: update_slider_from_entry(duty_cycle_entry, duty_cycle_scale) or update_duty_cycle(duty_cycle_entry.get()))

duty_cycle_unit_label = tk.Label(config_frame, text="%")
duty_cycle_unit_label.place(x=400, y=110)

duty_cycle_entry.bind("<Return>", on_duty_cycle_entry_change)
duty_cycle_entry.bind("<FocusOut>", on_duty_cycle_entry_change)

# Pulse Chain Configuration Button
pulse_chain_button = tk.Button(config_frame, text="Pulse Chain Config", command=open_pulse_chain_config)
pulse_chain_button.place(x=10, y=160)

# Pulse Chain Configuration Display
pulse_chain_display = tk.Text(config_frame, height=10, width=15, wrap='word', state=tk.DISABLED)
pulse_chain_display.place(x=10, y=200)


# Scrollbar for the Pulse Chain
scrollbar = tk.Scrollbar(config_frame, command=pulse_chain_display.yview)
scrollbar.place(in_=pulse_chain_display, relx=1, rely=0, relheight=1, anchor='ne')
pulse_chain_display['yscrollcommand'] = scrollbar.set


#time_frame
stopwatch_display = tk.Label(time_frame, text="Stopwatch: 00:00:00.000", bg='white')
stopwatch_display.place(x=10, y=10)

# Real-Time Clock display
real_time_clock = tk.Label(time_frame, text="", bg='white', font=("Helvetica", 18))
real_time_clock.place(x=225, y=10)
update_clock()

# Data Log Window


data_log_window = tk.Text(time_frame, height=20, width=50, font=("Helvetica", 10))
data_log_window.place(x=10, y=50)
data_log_window.config(state=tk.DISABLED)


data_log_scrollbar = tk.Scrollbar(time_frame, orient="vertical", command=data_log_window.yview)

data_log_scrollbar.place(x=390, y=50, height=320)
data_log_window.config(yscrollcommand=data_log_scrollbar.set)



data_log_window.config(yscrollcommand=data_log_scrollbar.set)
# Log the initial state of the application
update_data_log('Initialization')


#Orange frame
# Data button


# Settings button


# Help button
help_button = tk.Button(util_frame, text="Help", command=open_help_window)
help_button.place(x=265, y=90, width=100, height=30)

# Create the "Refresh" button in the util_frame
refresh_button = tk.Button(util_frame, text="Refresh", command=refresh_window)
# Assuming the size and placement to match other buttons like "Help" or "Settings"
refresh_button.place(x=265, y=130, width=100, height=30)


root.mainloop()
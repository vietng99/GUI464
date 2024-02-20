import tkinter as tk
from tkinter import ttk
import datetime
import time
import serial
import serial.tools.list_ports
##################################################################################################################################
ser = None

##################################################################################################################################

# Configuration storage
config_storage = {
    "frequency": None,
    "duty_cycle": None,
    "pulse_chain": []
}


def update_frequency(value):
    global ser  # Ensure ser is accessible globally
    config_storage["frequency"] = float(value)
    info_frequency_label.config(text=f"Frequency: {value} Hz")
    update_data_log("Frequency Updated", freq=value, duty_cycle=config_storage.get('duty_cycle', 'N/A'))
    root.update_idletasks()
    command = f"FREQ:{value}\n"
    # Check if ser is not None and the port is open before writing
    if ser is not None and ser.is_open:
        ser.write(command.encode())
    else:
        print("Serial port is not open.")



def update_duty_cycle(value):
    global ser  # Ensure ser is accessible globally
    config_storage["duty_cycle"] = float(value)
    info_duty_cycle_label.config(text=f"Duty Cycle: {value}%")
    update_data_log("Duty Cycle Updated", freq=config_storage.get('frequency', 'N/A'), duty_cycle=value)
    root.update_idletasks()
    command = f"DUTY:{value}\n"
    # Check if ser is not None and the port is open before writing
    if ser is not None and ser.is_open:
        ser.write(command.encode())
    else:
        print("Serial port is not open.")




def refresh_window():
    refresh_info_bar()
    root.update_idletasks()
    root.update()

def refresh_info_bar():
    # Assuming current_com_port and current_baud_rate are updated elsewhere in your application
    global current_com_port, current_baud_rate

    # Update the info bar labels with the latest values from config_storage or other state variables
    info_frequency_label.config(text=f"Frequency: {config_storage.get('frequency', '--')} Hz")
    info_duty_cycle_label.config(text=f"Duty Cycle: {config_storage.get('duty_cycle', '--')}%")
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
    data_log_window.insert(tk.END, "Duty Cycle=", "action")
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
    global ser, stopwatch_running, start_time, elapsed_time
    if not stopwatch_running:
        stopwatch_running = True
        # Adjust start_time to account for already elapsed time if any
        start_time = time.time()
        update_stopwatch_display()
    # Log the start action
    freq = config_storage.get('frequency', 'N/A')
    duty_cycle = config_storage.get('duty_cycle', 'N/A')
    update_data_log('start', freq, duty_cycle)

    #ser
    if ser is not None and ser.is_open:
        ser.write("START\n".encode())
    else:
        print("Serial port is not open.")

def stop_command():
    global ser, stopwatch_running, elapsed_time, start_time
    if stopwatch_running:
        # Calculate and update elapsed_time based on the current period
        elapsed_time += time.time() - start_time
        stopwatch_running = False
        # Reset start_time to None to avoid using stale value
        start_time = None

    #ser
    if ser is not None and ser.is_open:
        ser.write("STOP\n".encode())
    else:
        print("Serial port is not open.")

    # Log the stop action
    freq = config_storage.get('frequency', 'N/A')
    duty_cycle = config_storage.get('duty_cycle', 'N/A')
    update_data_log('stop', freq, duty_cycle)

def reset_command():
    global ser, elapsed_time, start_time, stopwatch_running
    # Reset elapsed time to 0 and ensure stopwatch is marked as not running
    elapsed_time = 0
    stopwatch_running = False
    start_time = None  # Also reset start_time to avoid any confusion
    #ser
    if ser is not None and ser.is_open:
        ser.write("RESET\n".encode())
    else:
        print("Serial port is not open.")

    # Update the display to show the reset state
    update_stopwatch_display()
    stopwatch_display.config(text="Stopwatch: 00:00:00.000")

    # Additional reset actions (unrelated to the stopwatch issue)
    config_storage["frequency"] = None
    config_storage["duty_cycle"] = None
    frequency_scale.set(1700)  # Reset slider to a neutral position
    duty_cycle_scale.set(30)  # Reset slider to a neutral position
    frequency_entry.delete(0, tk.END)  # Clear the entry box
    duty_cycle_entry.delete(0, tk.END)  # Clear the entry box
    info_frequency_label.config(text="Frequency: -- Hz")
    info_duty_cycle_label.config(text="Duty Cycle: --%")
    update_data_log("Reset", freq="N/A", duty_cycle="N/A")

    root.update_idletasks()



#still trying to find a way to fix the stopwatch, for now, every time stop then start again, it double the time

def save_as_preset_command():
    pass


def open_presets_list_command():
    pass

def load_preset_command():
    pass
def open_pulse_chain_config():
    new_window = tk.Toplevel(root)
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
        row_widgets = {}

        entry = tk.Entry(scrollable_frame, width=25, validate='key', validatecommand=validate_command)
        entry.grid(row=row_number, column=1, padx=10, pady=10)
        row_widgets['entry'] = entry

        switch_var = tk.BooleanVar()
        toggle = tk.Checkbutton(scrollable_frame, text="Off", bg="red", variable=switch_var,
                                onvalue=True, offvalue=False, command=lambda: toggle_switch(toggle, switch_var))
        toggle.grid(row=row_number, column=2, padx=10, pady=10)
        row_widgets['toggle'] = toggle

        rows.append(row_widgets)

    def delete_last_row():
        if rows:
            last_row = rows.pop()
            last_row['entry'].destroy()
            last_row['toggle'].destroy()

    def toggle_switch(switch, var):
        if var.get():
            switch.config(text="On", bg="green")
        else:
            switch.config(text="Off", bg="red")

    def close_window():
        pulse_chain_config = []
        for row in rows:
            entry_value = row['entry'].get()  # Get the pulse count from the entry
            switch_state = row['toggle'].cget('text')
            # Convert 'On'/'Off' text to a boolean or keep as string based
            state = True if switch_state == "On" else False
            # Create a dictionary for the configuration
            config_entry = {"count": int(entry_value) if entry_value.isdigit() else 0, "state": state}
            pulse_chain_config.append(config_entry)

        # Update the main configuration storage
        config_storage["pulse_chain"] = pulse_chain_config

        # Update the display, adapting the function to handle the new structure
        update_pulse_chain_config(config_storage["pulse_chain"])

        new_window.destroy()

    add_row_button = tk.Button(scrollable_frame, text="+", command=add_row, width=3, height=2)
    add_row_button.grid(row=0, column=3, padx=10, pady=10)

    delete_row_button = tk.Button(scrollable_frame, text="-", command=delete_last_row, width=3, height=2)
    delete_row_button.grid(row=0, column=4, padx=10, pady=10)

    add_row()  # Add the first row

    # Add the Confirm button to the window
    confirm_button = tk.Button(new_window, text="Confirm", command=close_window)
    confirm_button.pack(pady=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def update_pulse_chain_config(new_config):
    pulse_chain_display.config(state=tk.NORMAL)
    pulse_chain_display.delete(1.0, tk.END)
    formatted_config = '\n'.join([f"{item['count']} {'on' if item['state'] else 'off'}" for item in new_config])
    pulse_chain_display.insert(tk.END, formatted_config)
    pulse_chain_display.config(state=tk.DISABLED)


def validate_entry_input(P):
    # Allow only numeric input
    if P.isdigit() or P == "":
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

def open_data_window():
    data_window = tk.Toplevel(root)
    data_window.title("Data")


def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x300")  # Adjust size as needed

    # Function to refresh the list of COM ports
    def refresh_com_ports():
        com_ports = [comport.device for comport in serial.tools.list_ports.comports()]
        com_port_cb['values'] = com_ports
        if com_ports:
            com_port_cb.current(0)  # Set the first COM port as the current item
        else:
            com_port_cb.set('No COM Ports Found')

    # COM Port selection
    tk.Label(settings_window, text="Select COM Port:").pack(pady=10)
    com_port_cb = ttk.Combobox(settings_window, width=27)
    com_port_cb.pack()
    refresh_com_ports()  # Populate the combobox with available COM ports

    # Baud Rate selection
    tk.Label(settings_window, text="Select Baud Rate:").pack(pady=10)
    baud_rate_var = tk.StringVar()
    baud_rate_cb = ttk.Combobox(settings_window, textvariable=baud_rate_var,
                                values=[9600, 19200, 38400, 57600, 115200])
    baud_rate_cb.pack()
    baud_rate_cb.set("9600")  # Default value

    # Timeout entry
    tk.Label(settings_window, text="Enter Timeout (s):").pack(pady=10)
    timeout_var = tk.StringVar()
    timeout_entry = tk.Entry(settings_window, textvariable=timeout_var)
    timeout_entry.pack()
    timeout_var.set("1")  # Default value

    # Refresh Button - In case the COM ports change (e.g., plugging in a new device)
    refresh_button = tk.Button(settings_window, text="Refresh COM Ports", command=refresh_com_ports)
    refresh_button.pack(pady=10)

    # Apply Button - To apply the selected COM port, baud rate, and timeout
    def apply_settings():
        global ser  # Reference the global serial connection
        selected_com_port = com_port_cb.get()
        selected_baud_rate = baud_rate_var.get()
        selected_timeout = timeout_var.get()

        try:
            if ser is not None and ser.is_open:
                ser.close()  # Close the existing connection if open
            ser = serial.Serial(selected_com_port, baudrate=int(selected_baud_rate),
                                timeout=float(selected_timeout))
            print(
                f"Connected to {selected_com_port} with baud rate {selected_baud_rate} and timeout {selected_timeout}s")
            # Update UI or status to indicate successful connection

            # Update the info bar labels
            info_com_port_label.config(text=f"COM Port: {selected_com_port}")
            info_baud_rate_label.config(text=f"Baud Rate: {selected_baud_rate}")

        except serial.SerialException as e:
            print(f"Error connecting to {selected_com_port}: {e}")
            # Update UI or status to indicate failure
            info_com_port_label.config(text="COM Port: Connection Failed")
            info_baud_rate_label.config(text="Baud Rate: --")

    apply_button = tk.Button(settings_window, text="Apply", command=apply_settings)
    apply_button.pack(pady=10)


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


def connect_command():
    dynamic_status_label.config(text="Connected", fg='green')


def disconnect_command():
    dynamic_status_label.config(text="Disconnected", fg='red')


def open_presets_list_command():
    presets_window = tk.Toplevel(root)
    presets_window.title("Presets List")
    presets_window.geometry("400x300")


    tk.Label(presets_window, text="List of Presets:").pack()

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





# Flag to control border visibility
border_visible = False  # Set to False for invisible borders, True for visible

# Initialize the main window
root = tk.Tk()
root.title('GUI')
root.geometry('1200x800')

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

# Add an information bar below the dynamic display
info_bar = tk.Label(display_frame, bg='white', height=30, width=800, highlightbackground='black', highlightthickness=1)
info_bar.pack(side='bottom', fill='x')

info_frequency_label = tk.Label(info_bar, text="Frequency: --", bg='white')
info_duty_cycle_label = tk.Label(info_bar, text="Duty Cycle: --", bg='white')
info_current_runtime_label = tk.Label(info_bar, text="Current Runtime: --", bg='white')
info_expected_runtime_label = tk.Label(info_bar, text="Expected Runtime: --", bg='white')
#info_preset_name_label = tk.Label(info_bar, text="Preset: None", bg='white')
info_com_port_label = tk.Label(info_bar, text="COM Port: N/A", bg='white')
info_baud_rate_label = tk.Label(info_bar, text="Baud Rate: --", bg='white')


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


# Frequency Adjustment UI Components
frequency_label = tk.Label(config_frame, text="Frequency Adjustment")
frequency_label.place(x=10, y=60)

frequency_scale = tk.Scale(config_frame, from_=50, to=5000, orient='horizontal', length=200)
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
duty_cycle_label = tk.Label(config_frame, text="Duty Cycle Control")
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
pulse_chain_display = tk.Text(config_frame, height=10, width=10, wrap='word', state=tk.DISABLED)
pulse_chain_display.place(x=10, y=200)


# Scrollbar for the Pulse Chain
scrollbar = tk.Scrollbar(config_frame, command=pulse_chain_display.yview)
scrollbar.place(in_=pulse_chain_display, relx=1, rely=0, relheight=1, anchor='ne')
pulse_chain_display['yscrollcommand'] = scrollbar.set

# Preset Management
save_as_preset_button = tk.Button(config_frame, text="Save as Preset", command=save_as_preset_command, width=15, height=2)
save_as_preset_button.place(x=10, y=420)

open_presets_list_button = tk.Button(config_frame, text="Open Presets List", command=open_presets_list_command, width=15, height=2)
open_presets_list_button.place(x=150, y=420)

load_preset_button = tk.Button(config_frame, text="Load Preset", command=load_preset_command, width=15, height=2)
load_preset_button.place(x=290, y=420)

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
data_button = tk.Button(util_frame, text="Data", command=open_data_window)
data_button.place(x=265, y=10, width=100, height=30)

# Settings button
settings_button = tk.Button(util_frame, text="Settings", command=open_settings_window)
settings_button.place(x=265, y=50, width=100, height=30)

# Help button
help_button = tk.Button(util_frame, text="Help", command=open_help_window)
help_button.place(x=265, y=90, width=100, height=30)

# Create the "Refresh" button in the util_frame
refresh_button = tk.Button(util_frame, text="Refresh", command=refresh_window)
# Assuming the size and placement to match other buttons like "Help" or "Settings"
refresh_button.place(x=265, y=130, width=100, height=30)

# Static Connection Status Label
static_status_label = tk.Label(util_frame, text="Connection Status: ", bg='white')
static_status_label.place(x=160, y=230)

# Dynamic Connection Status Label
dynamic_status_label = tk.Label(util_frame, text="Disconnected", fg='red', bg='white')
dynamic_status_label.place(x=280, y=230)

# Connect button
connect_button = tk.Button(util_frame, text="Connect", command=connect_command)
connect_button.place(x=155, y=260, width=100, height=30)

# Disconnect button
disconnect_button = tk.Button(util_frame, text="Disconnect", command=disconnect_command)
disconnect_button.place(x=265, y=260, width=100, height=30)

# Start the Tkinter event loop
root.mainloop()
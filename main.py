import tkinter as tk
import datetime

# Flag to control border visibility
border_visible = False  # Set to False for invisible borders, True for visible

def get_border_color(original_color):
    return original_color if border_visible else 'white'

def update_clock():
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Format time with milliseconds
    real_time_clock.config(text=now)
    real_time_clock.after(10, update_clock)  # Update the time every 50 milliseconds

def update_data_log(new_data):
    data_log_window.config(state=tk.NORMAL)  # Enable editing of the widget
    data_log_window.insert(tk.END, new_data + "\n")  # Add new data
    data_log_window.config(state=tk.DISABLED)  # Disable editing of the widget


# Button commands placeholders
def start_command():
    pass

def stop_command():
    pass

def reset_command():
    pass
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

    add_row_button = tk.Button(scrollable_frame, text="+", command=add_row, width=3, height=2)
    add_row_button.grid(row=0, column=3, padx=10, pady=10)

    delete_row_button = tk.Button(scrollable_frame, text="-", command=delete_last_row, width=3, height=2)
    delete_row_button.grid(row=0, column=4, padx=10, pady=10)

    add_row()  # Add the first row

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Validation
def validate_entry_input(P):
    return P.isdigit() or P == ""

def update_pulse_chain_config(new_config):
    pulse_chain_display.config(state=tk.NORMAL)  # Enable text widget for editing
    pulse_chain_display.delete(1.0, tk.END)  # Clear existing text
    formatted_config = '\n'.join(new_config)  # Format each item on a new line
    pulse_chain_display.insert(tk.END, formatted_config)  # Insert formatted configuration
    pulse_chain_display.config(state=tk.DISABLED)  # Set back to read-only

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

def open_help_window():
    help_window = tk.Toplevel(root)
    help_window.title("Help")


# Placeholder functions for button commands
def connect_command():
    dynamic_status_label.config(text="Connected", fg='green')


def disconnect_command():
    dynamic_status_label.config(text="Disconnected", fg='red')


def open_presets_list_command():
    presets_window = tk.Toplevel(root)
    presets_window.title("Presets List")
    presets_window.geometry("400x300")


    tk.Label(presets_window, text="List of Presets:").pack()


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

frequency_label = tk.Label(info_bar, text="Frequency: --", bg='white')
duty_cycle_label = tk.Label(info_bar, text="Duty Cycle: --", bg='white')
current_runtime_label = tk.Label(info_bar, text="Current Runtime: --", bg='white')
expected_runtime_label = tk.Label(info_bar, text="Expected Runtime: --", bg='white')
preset_name_label = tk.Label(info_bar, text="Preset: None", bg='white')


frequency_label.pack(side='left', padx=10)
duty_cycle_label.pack(side='left', padx=10)
current_runtime_label.pack(side='left', padx=10)
expected_runtime_label.pack(side='left', padx=10)
preset_name_label.pack(side='left', padx=10)

#Green Frame
start_button = tk.Button(config_frame, text="Start", command=start_command, width=10, height=2)
start_button.place(x=10, y=10)

stop_button = tk.Button(config_frame, text="Stop", command=stop_command, width=10, height=2)
stop_button.place(x=110, y=10)

reset_button = tk.Button(config_frame, text="Reset", command=reset_command, width=10, height=2)
reset_button.place(x=220, y=10)

# Frequency Control
frequency_label = tk.Label(config_frame, text="Frequency Adjustment")
frequency_label.place(x=10, y=60)
frequency_scale = tk.Scale(config_frame, from_=50, to=5000, orient='horizontal', length=200, command=lambda value: update_entry_from_slider(frequency_scale, frequency_entry))
frequency_scale.place(x=150, y=60)
frequency_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
frequency_entry.place(x=360, y=60)
frequency_entry.bind("<Return>", lambda event: update_slider_from_entry(frequency_entry, frequency_scale))
frequency_unit_label = tk.Label(config_frame, text="Hz")
frequency_unit_label.place(x=400, y=60)

# Duty Cycle Control
duty_cycle_label = tk.Label(config_frame, text="Duty Cycle Control")
duty_cycle_label.place(x=10, y=110)
duty_cycle_scale = tk.Scale(config_frame, from_=0, to=100, orient='horizontal', length=200, command=lambda value: update_entry_from_slider(duty_cycle_scale, duty_cycle_entry))
duty_cycle_scale.place(x=150, y=110)
duty_cycle_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
duty_cycle_entry.place(x=360, y=110)
duty_cycle_entry.bind("<Return>", lambda event: update_slider_from_entry(duty_cycle_entry, duty_cycle_scale))
duty_cycle_unit_label = tk.Label(config_frame, text="%")
duty_cycle_unit_label.place(x=400, y=110)

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

# Stopwatch display (placeholder for now)
stopwatch_display = tk.Label(time_frame, text="Stopwatch: 00:00:00.000", bg='white')
stopwatch_display.place(x=10, y=10)

# Real-Time Clock display
real_time_clock = tk.Label(time_frame, text="", bg='white', font=("Helvetica", 18))
real_time_clock.place(x=225, y=10)
update_clock()

# Data Log Window
data_log_window = tk.Text(time_frame, height=15, width=45)
data_log_window.place(x=10, y=50)
data_log_window.config(state=tk.DISABLED)

# Example update to data log
update_data_log("Initial log entry.")

# Example pulse chain configuration
pulse_chain_example = [
    "1 on", "2 off", "1 on", "3 off", "3 on",
    "2 off", "1 on", "4 off", "1 on", "1 off",
    "1 on", "1 off", "2 on", "3 off"
]
update_pulse_chain_config(pulse_chain_example)

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

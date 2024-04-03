import tkinter as tk
import datetime
import time
import serial
import serial.tools.list_ports
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ser = None
border_visible = False

config_storage = {
    "frequency": None,
    "duty_cycle": None,
    "pulse_chain": []
}

def update_frequency(value):
    config_storage["frequency"] = float(value)
    info_frequency_label.config(text=f"Frequency: {value} Hz")
    root.update_idletasks()

def update_duty_cycle(value):
    config_storage["duty_cycle"] = float(value)
    info_duty_cycle_label.config(text=f"Duty Cycle: {value}%")
    root.update_idletasks()

def refresh_window():
    refresh_info_bar()
    root.update_idletasks()
    root.update()

def refresh_info_bar():
    info_frequency_label.config(text=f"Frequency: {config_storage.get('frequency', '--')} Hz")
    info_duty_cycle_label.config(text=f"Duty Cycle: {config_storage.get('duty_cycle', '--')}%")
    info_current_runtime_label.config(text=f"Current Runtime: {config_storage.get('current_runtime', '--')}")
    info_expected_runtime_label.config(text=f"Expected Runtime: {config_storage.get('expected_runtime', '--')}")
    info_preset_name_label.config(text=f"Preset: {config_storage.get('preset_name', 'None')}")
    root.update_idletasks()

def get_border_color(original_color):
    return original_color if border_visible else 'white'

def update_clock():
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    real_time_clock.config(text=now)
    real_time_clock.after(10, update_clock)

stopwatch_running = False
start_time = None
elapsed_time = 0

def update_stopwatch_display():
    if stopwatch_running:
        current_time = time.time()
        total_elapsed = elapsed_time + (current_time - start_time)
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(total_elapsed)) + f'.{str(int(total_elapsed * 1000) % 1000).zfill(3)}'
        stopwatch_display.config(text=f"Stopwatch: {formatted_time}")
        root.after(10, update_stopwatch_display)

def update_data_log(new_data):
    data_log_window.config(state=tk.NORMAL)
    data_log_window.insert(tk.END, new_data + "\n")
    data_log_window.config(state=tk.DISABLED)

def start_command():
    global stopwatch_running, start_time, elapsed_time
    if not stopwatch_running:
        stopwatch_running = True
        start_time = time.time() - elapsed_time
        update_stopwatch_display()

def stop_command():
    global stopwatch_running, elapsed_time
    if stopwatch_running:
        stopwatch_running = False
        elapsed_time += time.time() - start_time

def reset_command():
    global elapsed_time, start_time
    elapsed_time = 0
    if stopwatch_running:
        start_time = time.time()
    update_stopwatch_display()
    stopwatch_display.config(text="Stopwatch: 00:00:00.000")

def save_as_preset_command():
    pass

def open_presets_list_command():
    pass

def load_preset_command():
    pass

def open_pulse_chain_config():
    new_window = tk.Toplevel()
    new_window.title("Pulse Chain Configuration")
    new_window.geometry("600x400")

    canvas = tk.Canvas(new_window, borderwidth=0)
    scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    rows = []

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
        pulse_chain_values = [int(row['entry'].get()) for row in rows if row['entry'].get().isdigit()]
        config_storage["pulse_chain"] = pulse_chain_values
        new_window.destroy()

    add_row_button = tk.Button(scrollable_frame, text="+", command=add_row, width=3, height=2)
    add_row_button.grid(row=0, column=3, padx=10, pady=10)

    delete_row_button = tk.Button(scrollable_frame, text="-", command=delete_last_row, width=3, height=2)
    delete_row_button.grid(row=0, column=4, padx=10, pady=10)

    add_row()

    confirm_button = tk.Button(new_window, text="Confirm", command=close_window)
    confirm_button.pack(pady=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def update_pulse_chain_config(new_config_str):
    pulse_chain_display.config(state=tk.NORMAL)
    pulse_chain_display.delete(1.0, tk.END)

    durations = new_config_str.split(", ")
    formatted_config = '\n'.join([f"{durations[i]} {'on' if i % 2 == 0 else 'off'}" for i in range(len(durations))])
    pulse_chain_display.insert(tk.END, formatted_config)
    pulse_chain_display.config(state=tk.DISABLED)

def validate_entry_input(P):
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
    help_window.geometry("1200x900")

    help_text = tk.Text(help_window, wrap="word")
    help_text.pack(expand=True, fill="both", padx=10, pady=10)

    help_content = """
    [Your Help Content]
    """

    help_text.insert("1.0", help_content)
    help_text.config(state="disabled")

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

root = tk.Tk()
root.title('GUI')
root.geometry('1200x800')

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

dynamic_display = tk.Canvas(display_frame, bg='lightgrey', height=280, width=800, highlightbackground='black', highlightthickness=1)
dynamic_display.pack()

info_bar = tk.Label(display_frame, bg='white', height=30, width=800, highlightbackground='black', highlightthickness=1)
info_bar.pack(side='bottom', fill='x')

info_frequency_label = tk.Label(info_bar, text="Frequency: --", bg='white')
info_duty_cycle_label = tk.Label(info_bar, text="Duty Cycle: --", bg='white')
info_current_runtime_label = tk.Label(info_bar, text="Current Runtime: --", bg='white')
info_expected_runtime_label = tk.Label(info_bar, text="Expected Runtime: --", bg='white')
info_preset_name_label = tk.Label(info_bar, text="Preset: None", bg='white')

info_frequency_label.pack(side='left', padx=10)
info_duty_cycle_label.pack(side='left', padx=10)
info_current_runtime_label.pack(side='left', padx=10)
info_expected_runtime_label.pack(side='left', padx=10)
info_preset_name_label.pack(side='left', padx=10)

start_button = tk.Button(config_frame, text="Start", command=start_command, width=10, height=2)
start_button.place(x=10, y=10)

stop_button = tk.Button(config_frame, text="Stop", command=stop_command, width=10, height=2)
stop_button.place(x=110, y=10)

reset_button = tk.Button(config_frame, text="Reset", command=reset_command, width=10, height=2)
reset_button.place(x=220, y=10)

frequency_label = tk.Label(config_frame, text="Frequency Adjustment")
frequency_label.place(x=10, y=60)

frequency_scale = tk.Scale(config_frame, from_=50, to_= 5000, orient='horizontal', length=200, command=update_frequency)
frequency_scale.place(x=150, y=60)

frequency_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
frequency_entry.place(x=360, y=60)
frequency_entry.bind("<Return>", lambda event: update_slider_from_entry(frequency_entry, frequency_scale) or update_frequency(frequency_entry.get()))

frequency_unit_label = tk.Label(config_frame, text="Hz")
frequency_unit_label.place(x=400, y=60)

duty_cycle_label = tk.Label(config_frame, text="Duty Cycle Control")
duty_cycle_label.place(x=10, y=110)

duty_cycle_scale = tk.Scale(config_frame, from_=0, to_=100, orient='horizontal', length=200, command=update_duty_cycle)
duty_cycle_scale.place(x=150, y=110)

duty_cycle_entry = tk.Entry(config_frame, width=7, validate='key', validatecommand=validate_command)
duty_cycle_entry.place(x=360, y=110)
duty_cycle_entry.bind("<Return>", lambda event: update_slider_from_entry(duty_cycle_entry, duty_cycle_scale) or update_duty_cycle(duty_cycle_entry.get()))

duty_cycle_unit_label = tk.Label(config_frame, text="%")
duty_cycle_unit_label.place(x=400, y=110)

pulse_chain_button = tk.Button(config_frame, text="Pulse Chain Config", command=open_pulse_chain_config)
pulse_chain_button.place(x=10, y=160)

pulse_chain_display = tk.Text(config_frame, height=10, width=10, wrap='word', state=tk.DISABLED)
pulse_chain_display.place(x=10, y=200)

scrollbar = tk.Scrollbar(config_frame, command=pulse_chain_display.yview)
scrollbar.place(in_=pulse_chain_display, relx=1, rely=0, relheight=1, anchor='ne')
pulse_chain_display['yscrollcommand'] = scrollbar.set

save_as_preset_button = tk.Button(config_frame, text="Save as Preset", command=save_as_preset_command, width=15, height=2)
save_as_preset_button.place(x=10, y=420)

open_presets_list_button = tk.Button(config_frame, text="Open Presets List", command=open_presets_list_command, width=15, height=2)
open_presets_list_button.place(x=150, y=420)

load_preset_button = tk.Button(config_frame, text="Load Preset", command=load_preset_command, width=15, height=2)
load_preset_button.place(x=290, y=420)

stopwatch_display = tk.Label(time_frame, text="Stopwatch: 00:00:00.000", bg='white')
stopwatch_display.place(x=10, y=10)

real_time_clock = tk.Label(time_frame, text="", bg='white', font=("Helvetica", 18))
real_time_clock.place(x=225, y=10)
update_clock()

data_log_window = tk.Text(time_frame, height=15, width=45)
data_log_window.place(x=10, y=50)
data_log_window.config(state=tk.DISABLED)

update_data_log("Initial log entry.")

data_button = tk.Button(util_frame, text="Data", command=open_data_window)
data_button.place(x=265, y=10, width=100, height=30)

settings_button = tk.Button(util_frame, text="Settings", command=open_settings_window)

# Start the Tkinter event loop
root.mainloop()
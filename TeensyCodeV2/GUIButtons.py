from TeensyGUI import find_serial_port, run_for_duration, send_to_device, update_serial_ports, change_baud_rate, stop_sequence, reset_parameters, preview_sequence, preview_button
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import warnings
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox


# Main application setup
root = tk.Tk()
root.title("Device Input GUI")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Main')
tab_control.add(tab2, text='Settings')
tab_control.pack(expand=1, fill="both")

sequence_size_var = tk.StringVar()
frequency_var = tk.StringVar()
duty_cycle_var = tk.StringVar()
sequence_var = tk.StringVar()

# Adjustments to ensure widgets are added to `tab1` using `grid`
ttk.Label(tab1, text="Sequence Size:").grid(column=0, row=0, sticky=tk.W)
sequence_size_entry = ttk.Entry(tab1, textvariable=sequence_size_var)
sequence_size_entry.grid(column=1, row=0)

ttk.Label(tab1, text="Frequency:").grid(column=0, row=1, sticky=tk.W)
frequency_entry = ttk.Entry(tab1, textvariable=frequency_var)
frequency_entry.grid(column=1, row=1)

ttk.Label(tab1, text="Duty Cycle:").grid(column=0, row=2, sticky=tk.W)
duty_cycle_entry = ttk.Entry(tab1, textvariable=duty_cycle_var)
duty_cycle_entry.grid(column=1, row=2)

ttk.Label(tab1, text="Sequence (comma-separated):").grid(column=0, row=3, sticky=tk.W)
sequence_entry = ttk.Entry(tab1, textvariable=sequence_var)
sequence_entry.grid(column=1, row=3)

# Add to the GUI setup
timer_duration_var = tk.StringVar()
ttk.Label(tab1, text="Duration (ms):").grid(column=0, row=8, sticky=tk.W)
timer_duration_entry = ttk.Entry(tab1, textvariable=timer_duration_var)
timer_duration_entry.grid(column=1, row=8)


ttk.Button(tab1, text="Start", command=send_to_device).grid(column=1, row=5, pady=10)
ttk.Button(tab1, text="Stop/Kill", command=stop_sequence).grid(column=1, row=6)
ttk.Button(tab1, text="Reset", command=reset_parameters).grid(column=1, row=7)

# The "Preview Sequence" button also needs to be added to `tab1` using `grid`
preview_button = ttk.Button(tab1, text="Preview Sequence", command=preview_sequence)
preview_button.grid(column=1, row=4, pady=10)


# Settings Tab
ttk.Label(tab2, text="Select Serial Port:").grid(column=0, row=0, sticky=tk.W)
port_combobox = ttk.Combobox(tab2)
port_combobox.grid(column=1, row=0)
update_serial_ports()

ttk.Label(tab2, text="Select Baud Rate:").grid(column=0, row=1, sticky=tk.W)
baud_rates = ["9600", "19200", "38400", "57600", "115200"]
baud_rate_combobox = ttk.Combobox(tab2, values=baud_rates)
baud_rate_combobox.current(0)  # default to 9600
baud_rate_combobox.grid(column=1, row=1)
baud_rate_combobox.bind("<<ComboboxSelected>>", change_baud_rate)

root.mainloop()
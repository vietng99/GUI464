import tkinter as tk
from tkinter import ttk
import serial
import threading
from GUIfunctions import find_serial_port, send_to_device, stop_sequence, reset_parameters, preprocess_sequence

def update_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_list = [port.device for port in ports]
    port_combobox['values'] = port_list
    if port_list:
        port_combobox.current(0)

def change_baud_rate(event):
    global ser
    selected_baud = baud_rate_combobox.get()
    ser.baudrate = selected_baud
    print(f"Baud rate changed to: {selected_baud}")

# GUI Setup
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
duration_var = tk.StringVar()

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

ttk.Label(tab1, text="Duration (s):").grid(column=0, row=4, sticky=tk.W)
duration_entry = ttk.Entry(tab1, textvariable=duration_var)
duration_entry.grid(column=1, row=4)

# preview_button = ttk.Button(tab1, text="Preview Sequence", command=preview_sequence)
# preview_button.grid(column=1, row=4, pady=10)

ttk.Button(tab1, text="Start", command=lambda: send_to_device(ser, sequence_size_var.get(), frequency_var.get(), duty_cycle_var.get(), sequence_var.get(), duration_var.get())).grid(column=1, row=5)
ttk.Button(tab1, text="Stop", command=lambda: stop_sequence(ser)).grid(column=1, row=6)
ttk.Button(tab1, text="Reset", command=lambda: reset_parameters(ser)).grid(column=1, row=7)

# Settings Tabttk.Label(tab2, text="Select Serial Port:").grid(column=0, row=0, sticky=tk.W)
port_combobox = ttk.Combobox(tab2)
port_combobox.grid(column=1, row=0)
update_serial_ports()

ttk.Label(tab2, text="Select Baud Rate:").grid(column=0, row=1, sticky=tk.W)
baud_rates = ["9600", "19200", "38400", "57600", "115200"]
baud_rate_combobox = ttk.Combobox(tab2, values=baud_rates)
baud_rate_combobox.current(0)  # default to 9600
baud_rate_combobox.grid(column=1, row=1)
baud_rate_combobox.bind("<<ComboboxSelected>>", change_baud_rate)

# Add Help Tab
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Help')
tab_control.pack(expand=1, fill="both")

# Help Content
help_text = """
Help Guide for Device Input GUI:

- Sequence Size: Enter the number of pulses in your sequence.
- Frequency: Specify the frequency for the pulse sequence in Hz.
- Duty Cycle: Enter the duty cycle as a percentage (0-100).
- Sequence: Input the sequence values as comma-separated numbers. Each number represents the duration of a pulse in milliseconds.
- Duration: Set the total duration for the sequence execution in seconds.
- Start Button: Click to send the current configuration and sequence to the Teensy board.
- Stop Button: Click to stop the current sequence execution immediately.
- Reset Button: Resets all input fields and the Teensy board to their default states.
- Serial Port: Select the serial port that your Teensy board is connected to.
- Baud Rate: Select the baud rate for serial communication. Make sure it matches the Teensy board settings.

Ensure your Teensy board is connected and configured correctly before sending commands.
"""

help_label = ttk.Label(tab3, text=help_text, justify="left", wraplength=500)
help_label.pack(padx=10, pady=10)


root.mainloop()

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

def find_serial_port():
    ports = [
        p.device
        for p in serial.tools.list_ports.comports()
    ]
    if not ports:
        raise IOError("No compatible device found - available ports: {}".format(
            [p.device for p in serial.tools.list_ports.comports()]))
    if len(ports) > 1:
        warnings.warn('Multiple devices found - using the first')
    return ports[0]

# try:
#     serialPort = find_serial_port()
#     baudRate = 9600
#     ser = serial.Serial(serialPort, baudRate)
#     # time.sleep(2)  # Delay to ensure the connection is ready
#     print(f"Device connected on {serialPort}")

# except Exception as e:
#     print(f"Error: {e}")
#     print(f"Details: {e.args}")
#     sys.exit(1)

# def run_for_duration(duration_ms):
#     start_time = time.time()
#     while (time.time() - start_time) * 1000 < duration_ms:
#         time.sleep(0.1)  # Sleep for a short time to avoid high CPU usage
#     stop_sequence()  # Stop the sequence after the duration

def send_to_device():
    sequence_size = sequence_size_var.get()
    frequency = frequency_var.get()
    duty_cycle = duty_cycle_var.get()
    sequence = sequence_var.get()
    data_str = f"<{sequence_size},{frequency},{duty_cycle},{sequence}>"
    sequence_var.set(data_str)  # Update the sequence preview
    print(f"Sending to device: {data_str}")  # Logging the data being sent

    # # Start the timer thread
    # duration_ms = int(timer_duration_var.get())
    # timer_thread = threading.Thread(target=run_for_duration, args=(duration_ms,))
    # timer_thread.start()
    try:
        ser.write(data_str.encode('utf-8'))
    except Exception as e:
        print(f"Error during send: {e}")
        print(f"Details: {e.args}")

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

def stop_sequence():
    try:
        ser.write(b"<0,0,0,0>")  # Example command to zero out the Teensy
        print("Teensy board zeroed out")
    except Exception as e:
        print(f"Error during stop: {e}")
        print(f"Details: {e.args}")


def reset_parameters():
    # Reset GUI fields
    sequence_size_var.set("")
    frequency_var.set("")
    duty_cycle_var.set("")
    sequence_var.set("")
    # Send reset command to Teensy
    try:
        ser.write(b"<0,0,0,0>")  # Assuming this command resets the Teensy
        print("Teensy board and GUI reset to clean state")
    except Exception as e:
        print(f"Error during reset: {e}")
        print(f"Details: {e.args}")

def generate_waveform():
    # Extracting the sequence parameters
    sequence_size = int(sequence_size_var.get())
    frequency = float(frequency_var.get())
    duty_cycle = float(duty_cycle_var.get()) / 100  # Convert percentage to a fraction
    sequence_str = sequence_var.get().split(',')  # Splitting the sequence into a list
    
    # Calculating the time period of one cycle (in seconds)
    period = 1 / frequency

    # Initialize time and amplitude arrays
    t = [0]  # Time starts at 0
    y = [0]  # Assume the waveform starts at 0 amplitude

    current_time = 0
    for i, duration in enumerate(map(int, sequence_str)):
        if i >= sequence_size:
            break  # Stop if the sequence size limit is reached
        
        duration_time = duration * period  # Convert duration units to time
        
        if i % 2 == 0:  # 'On' state
            next_time = current_time + duration_time * duty_cycle
            t.extend([current_time, next_time])
            y.extend([1, 1])  # Assuming amplitude 1 for 'on' state
            current_time = next_time
            
            # Adding the off part of the duty cycle
            off_time = current_time + duration_time * (1 - duty_cycle)
            t.append(off_time)
            y.append(0)  # Back to 0 amplitude
        else:  # 'Off' state, just extend the time without changing the amplitude
            next_time = current_time + duration_time
            t.extend([current_time, next_time])
            y.extend([0, 0])
            
        current_time = next_time
    
    return t, y


def preview_sequence():
    # Create a new top-level window for the preview display
    preview_window = tk.Toplevel(root)
    preview_window.title("Preview Display")
    window_width = 800
    window_height = 600
    preview_window.geometry(f"{window_width}x{window_height}")

    # Calculate the position for the new window (right side of the main window)
    main_x, main_y, main_width = root.winfo_x(), root.winfo_y(), root.winfo_width()
    gap = 20
    new_x, new_y = main_x + main_width + gap, main_y
    preview_window.geometry(f"+{new_x}+{new_y}")

    # Create a matplotlib figure
    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)

    # Generate sample data to plot (Replace this with your actual data)
    t, y = generate_waveform()

    # Plotting the data
    ax.plot(t, y)
    ax.set_title('Pulse Chain Visualization')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')

    # Embedding the matplotlib figure in the tkinter window
    canvas = FigureCanvasTkAgg(figure, master=preview_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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

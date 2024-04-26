import serial
import serial.tools.list_ports
import warnings
import sys

def find_serial_port():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    if not ports:
        raise IOError("No compatible device found - available ports: {}".format(
            [p.device for p in serial.tools.list_ports.comports()]))
    if len(ports) > 1:
        warnings.warn('Multiple devices found - using the first')
    return ports[0]

def preprocess_sequence(sequence):
    processed_sequence = ','.join([str(float(num) * 1000) for num in sequence.split(',')])
    return processed_sequence

def send_to_device(ser, sequence_size, frequency, duty_cycle, sequence, duration):
    processed_sequence = preprocess_sequence(sequence)
    data_str = f"<{sequence_size},{frequency},{duty_cycle},{duration},{processed_sequence}>"
    print(f"Sending to device: {data_str}")  # Logging the data being sent
    try:
        ser.write(data_str.encode('utf-8'))
    except Exception as e:
        print(f"Error during send: {e}")
        print(f"Details: {e.args}")

def stop_sequence(ser):
    try:
        ser.write(b"<0,0,0,0,0>")  
        print("Teensy board zeroed out")
    except Exception as e:
        print(f"Error during stop: {e}")
        print(f"Details: {e.args}")

def reset_parameters(ser):
    try:
        ser.write(b"<0,0,0,0,0>")  
        print("Teensy board and GUI reset to clean state")
    except Exception as e:
        print(f"Error during reset: {e}")
        print(f"Details: {e.args}")
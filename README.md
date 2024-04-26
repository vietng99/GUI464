# Electronic Model and Laser Interface

## Overview
This project provides an innovative solution for interfacing an electronic model with a laser unit for precision control applications. The system leverages a Python-based software application and custom firmware for the Teensy board to allow users to adjust the pulse width modulation (PWM) parameters, enabling highly specific control over laser operations. This setup is ideal for applications in scientific research, industrial processes, and hobbyist projects where precise laser modulation is required.

## Features
- **Direct Interface**: Connect the electronic model to any computer via USB for easy communication.
- **Customizable PWM Settings**: Adjust the PWM parameters through a user-friendly software interface to meet diverse application needs.
- **Plug-and-Play**: Minimal setup required, designed to be operational right out of the box.

## Algorithms Used and Developed
### Teensy Microcontroller Firmware (TeensyCodeV3.ino)
- **Serial Data Parsing**: Parses incoming serial data to configure the device settings.
- **PWM Control**: Dynamically adjusts PWM frequency and duty cycle based on user input.
- **Sequence Management**: Executes defined sequences of PWM outputs to control the laser in precise patterns.

### Python Application (Main_finalized.py)
- **GUI Management**: Provides a comprehensive user interface using Tkinter for easy interaction and operation control.
- **Real-Time Data Visualization**: Integrates plotting tools for real-time monitoring and control adjustments.
- **Serial Communication**: Handles communication with the Teensy microcontroller, sending configuration data and receiving operation feedback.
- **Concurrency Management**: Utilizes threading to manage multiple operations simultaneously, ensuring smooth system performance.

## Installation and Setup

### System Requirements
- Compatible operating system (Windows, macOS, Linux)
- USB port available
- Python 3.x installed

### Unpacking and Initial Assembly
1. **Unboxing the Device**: 
   - Remove the electronic model and all accessories from the packaging.
   - Verify that all components listed on the packing slip are included.
  
### Installation of the Electronic Model
1. **Connecting to a Computer**:
   - Use the provided USB cable to connect the electronic model to your computer.
   - Ensure that the connection is secure and the computer recognizes the device.
2. **Software Installation**:
   - Download `Main_finalized.py` from our GitHub repository.
   - Navigate to the script location on your computer.
   - Run the script by opening a command prompt or terminal and typing:
     ```
     python Main_finalized.py
     ```
   - Follow the on-screen prompts to complete the setup.

### Device Configuration
1. **Connecting to the Laser**:
   - Connect the output port of the electronic model to the laser unit using the appropriate cable.
   - Ensure all connections are secure.
2. **Setting Preferences**:
   - Launch the python script.
   - Navigate to the ‘Settings’ or ‘Preferences’ menu.
   - Set the desired PWM parameters. Default settings are suitable for general use but can be adjusted as needed.

## Power-Up and Initial Test
1. **Powering the Device**:
   - Ensure both the electronic model and the connected laser are powered on.
   - Follow safe power-up procedures as specified for each unit.
2. **Conducting a Test Run**:
   - Use the software interface to initiate a test run.
   - Verify that the laser operates according to the set PWM parameters.
   - Adjust settings if necessary and retest until the desired operation is achieved.

## Troubleshooting
- **Teensy Board Issues**:
  - If the Teensy board is not functioning as expected, re-upload `TeensyCodeV3.ino` using the Arduino IDE. Ensure the correct ports are selected during the upload process.

## Contributing
We welcome contributions! Please feel free to fork the repository, make your changes, and submit a pull request. For more details, visit the contributing guide in our repository.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

 

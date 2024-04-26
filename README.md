# Electronic Model and Laser Interface

## Overview
This project provides a complete solution for interfacing an electronic model with a laser unit. The system includes a Python-based software application and firmware for the Teensy board, enabling precise control over the laser's pulse width modulation (PWM) parameters.

## Features
- **Direct Interface**: Easily connect the electronic model to any computer via USB.
- **Customizable PWM Settings**: Adjust the PWM parameters to suit specific requirements using our intuitive software interface.
- **Plug-and-Play**: No assembly required, with minimal setup needed to get started.

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

 

# Electronic Model and Laser Interface

## Engineering Addendum

### Quick Start
This project interfaces an electronic model with a laser unit, controlled via a Python application and Teensy microcontroller firmware, to adjust pulse width modulation (PWM) parameters for precise laser operations. 

1. **Setup**: Connect the electronic model to a computer via the included USB cable.
2. **Software Installation**: Download and run `Main_finalized.py` from the GitHub repository.
3. **Device Configuration**: Set up the device and laser as described in the installation section below.

### Project Overview
This system leverages a Python-based application and custom firmware to offer users control over laser operations through adjustable PWM settings. Designed for use in scientific research, industrial processes, and hobbyist projects, it provides a direct interface for precise modulation of laser outputs.

### Challenges and Insights
- Implementing robust communication between the software and the Teensy board was challenging, resolved by optimizing serial data protocols.
- Developing a user-friendly GUI that handled real-time data for device control was critical for enhancing user interaction.

### Current State and Future Work
The project is fully operational, with ongoing plans to integrate a current amplifier for higher power applications and refine the GUI for enhanced control features.

## Features
- **Direct Interface**: Easy connection to any computer via USB.
- **Customizable PWM Settings**: User-friendly interface for adjusting PWM parameters.
- **Plug-and-Play**: Designed for easy setup and immediate use.

## Algorithms Used and Developed
### Teensy Microcontroller Firmware (TeensyCodeV3.ino)
- **Serial Data Parsing**
- **PWM Control**
- **Sequence Management**

### Python Application (Main_finalized.py)
- **GUI Management**
- **Real-Time Data Visualization**
- **Serial Communication**
- **Concurrency Management**

## Installation and Setup

### System Requirements
- OS: Windows, macOS, Linux
- USB port
- Python 3.x

### Unpacking and Initial Assembly
1. **Unboxing the Device**: Remove the electronic model and all accessories from the packaging. Verify all components are included.

### Installation of the Electronic Model
1. **Connecting to a Computer**: Connect the device to your computer using the provided USB cable.
2. **Software Installation**:
   ```bash
   python Main_finalized.py

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

 

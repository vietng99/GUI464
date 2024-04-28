# Hardware Documentation for Integrated Laser and Electronic Model

## Hardware Components
- **Teensy 4.1**
- **Breadboards**
- **Wiring and connectors**

## Bill of Materials (BOM)

The following components are used in the construction of the Integrated Laser and Electronic Model:

| Item | Quantity | Description              | Unit Cost | Extended Cost |
|------|----------|--------------------------|-----------|---------------|
| 1    | 1        | Teensy 4.1               | $33.08    | $33.08        |
| 2    | 3        | TI SN74AC541             | $0.81     | $2.43         |
| 3    | 3        | FT260Q Buffer Chip       | $1.99     | $5.97         |
| 4    | 1        | 3D Printing Filament     | $19.99    | $19.99        |
| 5    | 1        | SanDisk 128GB Memory Card| $20.99    | $20.99        |
| 6    | 1        | SparkFun Bi-directional level shifter | $3.50    | $3.50         |
| 7    | 1        | Breadboard               | $8.99     | $8.99         |
| 8    | 2        | M/M Jumper Wire          | $2.10     | $4.20         |
| 9    | 1        | SparkFun Solderable Breadboard | $5.50 | $5.50     |
| 10   | 1        | USB-A to USB-C Adapter   | $4.50     | $4.50         |
| 11   | 4        | Brass Thread Insert      | $2.75     | $11.00        |
|      |          | **Total Cost**           |           | **$120.15**   |

This BOM reflects the materials required for the production of a beta version of the project. Components are selected to balance cost-efficiency with the necessary functionality for project requirements.


## Schematics
![image](https://github.com/vietng99/GUI464/assets/91101287/52ce51e1-affd-4d3f-a919-c782a5efa982)


## Power Requirements
- **Voltage**: 3.3V from Teensy
- **Current**: Approximately 75 mA

## Assembly Instructions
1. Assemble the Teensy on the breadboard as per the schematic.
2. Connect the USB-C cable to Teensy and the PC.
3. Ensure firmware (`TeensyCodeV3.ino`) is uploaded via the Arduino IDE.

## Teensy 4.1 Specifications Overview

The Teensy 4.1 microcontroller board is a high-performance upgrade from its predecessor, the Teensy 4.0, providing advanced features suitable for robust projects that require significant processing power, memory, and flexible connectivity options. This section outlines the key specifications and features of the Teensy 4.1, which is designed to meet the demands of both hobbyists and professional developers working on complex embedded systems.

### Core Processor and Speed

The Teensy 4.1 is powered by an ARM Cortex-M7 processor that operates at a speed of 600 MHz. This processor is part of the NXP iMXRT1062 chip, recognized as one of the fastest microcontrollers currently available, offering speeds up to ten times faster than the Teensy 3.2. The Cortex-M7 is notable for its dual-issue, superscalar architecture, capable of executing two instructions per clock cycle, enhancing its performance in processing-intensive applications.

### Memory

Teensy 4.1 significantly expands its memory capabilities compared to its predecessors:
- **RAM**: 1024K total, with 512K tightly coupled. This tightly coupled memory (TCM) allows for faster, single-cycle access, crucial for real-time applications.
- **Flash Memory**: 2048K total, with 64K reserved for recovery and EEPROM emulation. This is four times the flash memory available on Teensy 4.0, supporting more extensive programs and complex data storage needs.

Additional memory expansion is possible through two new solder pads on the bottom side of the board:
- **PSRAM SOIC-8 chip**: For volatile storage options.
- **QSPI Flash Memory**: For additional non-volatile memory needs.

### Connectivity and I/O

- **USB Ports**: Teensy 4.1 features two full-speed USB ports capable of 480 MBit/sec, facilitating multiple high-speed connections for peripherals such as keyboards, MIDI devices, and other USB-hosted hardware.
- **Ethernet**: 100 MB Ethernet PHY offers network connectivity, suitable for IoT applications requiring internet access.
- **Digital/Analog I/O**: Includes 40 digital pins, all interrupt capable, and 14 analog pins with 2 on-chip ADCs, providing extensive interfacing capabilities.
- **Audio**: Equipped with 2 I2S and 1 S/PDIF digital audio interfaces, allowing for high-quality audio applications.
- **Storage**: An SD card socket connected via SDIO for high-speed data storage and retrieval.
- **Additional Peripherals**: Includes SPI, I2C, Serial interfaces, CAN Bus (including CAN FD), and more.

### Advanced Features

- **FPU Support**: The Cortex-M7 includes a floating-point unit that supports both 32-bit and 64-bit operations, providing hardware-accelerated computations for functions that require floating-point precision.
- **Power Management**: Features dynamic clock scaling with support for changes in processor speed without disrupting the timing functions critical for real-time applications. Additionally, a power shut-off feature allows for complete power-down with a pushbutton, and the RTC keeps track of time even when powered down.
- **Programmable FlexIO**: The FlexIO can be configured for various input/output tasks, enhancing the flexibility and capability of custom peripheral device interactions.
- **Security and Safety Features**: Includes a cryptographic acceleration unit and a random number generator, enhancing security applications. 

### Design and Form Factor

- **Size**: Maintains the same form factor as the Teensy 3.6, measuring 2.4" by 0.7", which makes it compatible with existing setups designed for earlier versions of Teensy.
- **Peripherals Cross Triggering**: Enables complex hardware interaction patterns which are essential for advanced project designs.

### Additional Considerations

- **Teensy 4.1 does not come with pre-soldered headers, a USB cable, or a hub**, requiring additional purchases and assembly for many projects.
- **Extensive Community Support**: Documentation, tutorials, and a robust community can be found on the Teensy forums and the main website, which also includes detailed technical resources and guides.



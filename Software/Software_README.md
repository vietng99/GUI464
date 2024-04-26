# Software Documentation for Integrated Laser and Electronic Model

## Software Overview
The GUI application controls the Teensy 4.1 board to generate customizable pulse sequences for neural stimulation. It includes features such as frequency and duty cycle adjustment, real-time previews, and operational logs.

## Software Architecture
- **Main.py**: Primary module handling the GUI and integrating other modules.
- **Communication.py**: Manages serial communication between the PC and the Teensy.
- **Visualization.py**: Provides real-time updating of pulse previews.

### Flow Chart
(Include a flow chart showing the dependencies between these modules)

## Development and Build Tools
- **Python 3.8.1**
- **PySerial for serial communication**
- **Tkinter for GUI development**
- **Matplotlib for rendering previews**

## Installation Instructions
1. Install Python 3.8.1 and necessary libraries (`pip install pyserial matplotlib tkinter`).
2. Clone the repository and navigate to the software directory.
3. Run `python Main_finalized.py` to launch the application.


## Additional Notes
Refer to inline comments and the `docs/` directory for further documentation on the software's functionality and architecture.

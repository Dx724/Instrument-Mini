# InstruMini
## String instruments, modernized.
![Image of the InstruMini](media/img_right.jpg)
Despite their high prices, there really hasn't been much innovation in the category of stringed instruments. The build quality might be better or faster, but it's still the same idea: strings and a fretboard.

The InstruMini aims to demonstrate a modernized interface which allows for increased information density, and thus communication of more through less.

The number of notes in linearly proportional to the number of frets on a stringed instrument. On some wind instruments such as trumpets, the relation is quadratic. However, consider that each fret when represented via an electronic interface is simply a bit. Thus, the power of expression should scale exponentially with the number of controls.

## TODO: Table of Contents

# Setup
## Hardware
The device is composed of two main hardware subsystems. The performer's controls are monitored by a ESP32 microcontroller. This information is communicated to a Raspberry Pi via Serial, which then translates the commands into visual effects and OSC messages for Sonic Pi.

A Raspberry Pi 4 with 4GB of RAM running Raspbian GNU/Linux 10 (buster) was used. The ESP32 was a FreeNove ESP32-WROVER-DEV module.

## ESP32 Wiring
__Joystick__
1. Connect the +5V pin to the ESP32's 5V output pin
2. Connect the GND pin to the ESP32's GND pin
3. Connect the VRX and VRY pins to the ESP32's GPIO 13 and 12, respectively
4. Connect the SW pin (Z-axis button) to the ESP32's GPIO 14
   
__Buttons__
1. For each of the two buttons, connect one side to the ESP32's GND pin
2. Connect the other side of the "upper" button (further away from the joystick) to the ESP32's GPIO 18
3. Connect the other side of the "lower" button to the ESP32's GPIO 19

__Switch__
1. Connect one pin of the SPST switch to the ESP32's GND pin
   - If using a SPDT switch, simply connect the common pin to GND and one of the other pins as per step 2)
2. Connect the other pin of the SPST switch to the ESP32's GPIO

## Raspberry Pi Wiring
A FreeNove 8 RGB LED module was used for visual effects. Connect the LED module to the Raspberry Pi's GPIO as follows:
1. Connect module's 5V to Pi's 5V
2. Connect module's GND to Pi's GND
3. Connect module's Din to Pi's GPIO18

## Connecting the Subsystems
1. Connect from the micro USB port of the ESP32 to a USB port on Raspberry Pi
2. Connect from the 3.5mm jack of the Raspberry Pi to a speaker
   - Alternatively, a Bluetooth speaker can be used. See the section (TODO) for more details.

## Software Dependencies

## Running Manually

## Run on Boot

## Customization

## Future Work
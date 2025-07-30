# Pico Laser Tripwire 🚨💡

A Raspberry Pi Pico-based laser tripwire system that detects changes in ambient light using an LDR sensor and triggers a visual alert with LEDs. Designed for creative projects, desk setups, or simple security triggers.

## Features

- 📷 Light detection via photoresistor (LDR)
- 🔘 Button-activated desk light (on/off)
- ⚡ LED fade-in/out alert sequence
- 🧠 Smart alert triggering using lux percentage threshold
- 🖥️ Debug info printed in the console

## Hardware Required

- Raspberry Pi Pico
- LDR (photoresistor GL5516)
- WS2812 LED strip (64 LEDs)
- Push button
- Jumper wires
- Resistors (as needed)
- Light source (preferably a laser diode 5v / 5mW)


## Pin Configuration

| Component | GPIO Pin |
|-----------|----------|
| Photoresistor | 26 |
| LED strip (WS2812) | 22 |
| Button | 14 |

## Light Detection Logic

The system reads light intensity from the photoresistor and converts it into a percentage. If light levels drop below `trigger_value` (default `50.00`%), an alert is triggered through LED color fading.

## LED Color Logic

- Desk light color: Soft white (`255, 160, 135`)
- Alert start: Bright red fade to original state (on or off)

## How It Works

1. 💡 LDR monitors ambient light continuously.
2. 🖲️ The button toggles the desk light, but does not interfere with alert logic.
3. 📉 If the light drops below the threshold, the system initiates an alert.
4. 🌈 LEDs change to red then fade from red to white (Lights are On).
5. 🌈 LEDs change to red then fade from red to black (Lights are Off).

## Setup & Running

1. Connect all components to the Raspberry Pi Pico.
2. Flash the `laser_trip.py` script onto the board.
3. Open serial monitor for debugging output.
4. Watch LEDs respond to light changes and button input!

## Credits

Created by [SilentWoof](https://github.com/SilentWoof)  
Inspired by practical light-sensitive triggers and LED control using PIO on the Pico.

---

Enjoy tinkering with this light-activated tripwire project! 🛠️✨

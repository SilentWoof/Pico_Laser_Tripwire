# Pico Laser Tripwire 🚨💡

A Raspberry Pi Pico-based laser tripwire system that detects changes in ambient light using an LDR sensor and triggers a visual alert with LEDs. Designed for creative projects, desk setups, or simple security triggers.

## Features

- 📷 Light detection via photoresistor (LDR)
- 🔘 Switch-activated desk light (on/off)
- ⚡ LED fade-in/out alert sequence
- 🧠 Smart alert triggering using lux percentage threshold
- 🖥️ Debug info printed in the console

## Hardware Required

- Raspberry Pi Pico  
- LDR (photoresistor GL5516)  
- WS2812 LED strip (64 LEDs)  
- Toggle switch  
- Jumper wires  
- 10 kΩ resistor (used for LDR voltage divider)  
- Light source (preferably a laser diode 5 V / 5 mW)

## Circuit Notes

The LDR is wired in a voltage divider configuration with a 10 kΩ resistor connected between GPIO26 and GND. This setup ensures stable analog readings by pulling the ADC pin low when ambient light is minimal. As light increases, the LDR’s resistance drops, raising the voltage at GPIO26 and increasing the ADC value. This configuration allows the system to detect light interruptions (e.g., a laser beam being broken).

## Circuit Diagram (Text Representation)

```
  +3.3V
    |
   [LDR]
    |
   |----> GP26 (ADC)
    |
 [10kΩ Resistor]
    |
   GND

  Switch:
  [Toggle Switch]
     |
    GPIO14
     |
    GND

  WS2812 LED Strip:
  GPIO22 ---> DIN on LED strip
  +5V    ---> VCC on LED strip
  GND    ---> GND on LED strip
```

## 3D Printed Files

Included are 2 .3mf files that can be printed on a 3D printer.  
The files are a 6 mm tube for the laser emitter, and another tube for the LDR.  
The tubes help to regulate the ambient light to eliminate false positives.

## Pin Configuration

| Component           | GPIO Pin |
|---------------------|----------|
| Photoresistor       | 26       |
| LED strip (WS2812)  | 22       |
| Switch              | 14       |

## Light Detection Logic

The system reads light intensity from the photoresistor and converts it into a percentage. If light levels drop below `trigger_value` (default `50.00`%), an alert is triggered through LED color fading.

## LED Color Logic

- Desk light color: Soft white (`255, 160, 135`)
- Alert start: Bright red fade to original state (on or off)

## How It Works

1. 💡 LDR monitors ambient light continuously.  
2. 🖲️ The switch toggles the desk light, but does not interfere with alert logic.  
3. 📉 If the light drops below the threshold, the system initiates an alert.  
4. 🌈 LEDs change to red then fade from red to white (Lights are On).  
5. 🌈 LEDs change to red then fade from red to black (Lights are Off).

## Setup & Running

1. Connect all components to the Raspberry Pi Pico.  
2. Ensure the LDR and 10 kΩ resistor form a voltage divider between 3.3 V and GND, with the midpoint connected to GPIO26.  
3. Flash the `laser_trip.py` script onto the board.  
4. Open serial monitor for debugging output.  
5. Watch LEDs respond to light changes and switch input!

## Credits

Created by [SilentWoof](https://github.com/SilentWoof)  
Inspired by practical light-sensitive triggers and LED control using PIO on the Pico.

---

Enjoy tinkering with this light-activated tripwire project! 🛠️✨
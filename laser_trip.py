import array, time, utime
from machine import Pin, ADC
from rp2 import PIO, StateMachine, asm_pio


trigger_value = 50.00 # LDR Lux % To trigger alert
photoPIN = 68
def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100, 2)
    return light

# Button to switch desk light on and off. Will not stop alerts.
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

# LED Configuration
num_leds = 64 # Number of LEDs in string
led_pin = 22 # GPIO Pin of LEDs
brightness = 1.0 # Sets the brightness for the LED String

black = (0, 0, 0)
white = (255, 160, 135)
red = (255, 0, 0)

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on pin
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(led_pin))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(num_leds)])

def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(num_leds)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

#Function to print some values for debugging
def status():
    ldr_value = readLight(photoPIN)
    print("Button: {} | Color: {} | Alert: {} | LDR Value: {}".format(button.value(), desk_lights, alert, ldr_value))

while True:
    if button.value() == 1:
        desk_lights = white
    else:
        desk_lights = black
    time.sleep(0.1)
    
    ldr_value = readLight(photoPIN)
    if ldr_value < trigger_value:
        alert = True
        r = 255
        g = 0
        b = 0
        if button.value() == 1:
            timer_start = utime.ticks_ms() # Timer Start
            while g != 160 and b != 135:
                if g < 160:
                    g += 1
                if b < 130:
                    b += 1
                desk_lights = (r, g, b)
                pixels_fill(desk_lights)
                pixels_show()
#                status()
                time.sleep(0.011) # Adjust the fade time. With Status: 0.007, Without Status: 0.011 for 5 second fade.
            fader_time = (utime.ticks_diff(utime.ticks_ms(), timer_start))/1000 # Stop timer and find difference in seconds
            print("Fade To White Time: {}s".format(fader_time, )) # Print Time
        else:
            timer_start = utime.ticks_ms() # Timer Start
            while r > 0:
                r = r - 3
                desk_lights = (r, g, b)
                pixels_fill(desk_lights)
                pixels_show()
#                status()
                time.sleep(0.039) # Adjust the fade time. With Status: 0.034, Without Status: 0.039 for 5 second fade.
            fader_time = (utime.ticks_diff(utime.ticks_ms(), timer_start))/1000 # Stop timer and find difference in seconds
            print("Fade To Black Time: {}s".format(fader_time)) # Print Time
    else:
        alert = False
        pixels_fill(desk_lights)
        pixels_show()


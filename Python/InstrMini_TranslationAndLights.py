import serial, time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client
import board, neopixel

# CONFIGURATION BEGIN
SERIAL_PORT = "COM4" # Serial port -- check device manager or ports listing
# Options below are purely for customization
DEAD_ZONE = 500 # Increase this to require larger joystick movements for sound
# CONFIGURATION END

ADC_RANGE = 4096
ADC_CENTER = ADC_RANGE // 2
NUM_SECTORS = 5 # Sectors per instrument (number of notes plus one)
CONFIG_DEAD_ZONE = ADC_RANGE * 0.45 # Dead zone in config mode

def to_angle(j_x, j_y):
    return math.atan2(j_y, j_x)

def get_note(joy_x, joy_y):
    joy_x -= ADC_CENTER
    joy_y -= ADC_CENTER
    if (joy_x ** 2 + joy_y ** 2) < DEAD_ZONE ** 2:
        return None
    note_angle = to_angle(joy_x, joy_y)
    instrument = int(note_angle > 0)
    sect = round(abs(note_angle) // (math.pi / NUM_SECTORS))
    light_pos = abs(note_angle) / math.pi
    return (instrument, sect, light_pos)

def get_cfg(joy_x, joy_y):
    joy_x -= ADC_CENTER
    joy_y -= ADC_CENTER
    if (joy_x ** 2 + joy_y ** 2) < CONFIG_DEAD_ZONE ** 2:
        return None
    cfg_angle = to_angle(joy_x, joy_y)
    cfg_mode = int(cfg_angle > 0)
    cfg_value = abs(cfg_angle) / math.pi
    return (cfg_mode, cfg_value)

# Allows for "interpolation" regardless of input data rate
# For example, going from note 1 to note 3 will assume note 2 was also played
# in the "strum"
def range_between(a, b, to_chord): # From sector a to sector b
    if a < b: res = range(a, b) # Sector 0 to Sector 1 plays "String" 0
    else: res = range(b, a) # Sector 1 to Sector 0 plays "String" 0
    if not to_chord: # Single notes
        return [major_sixth[nt] for nt in res]
    else:
        return [chord_progression[nt] for nt in res]

def do_set_lights(color_arr):
    for i in range(8):
        pixels[i] = color_arr[i]
    print(pixels)

LIGHT_LOCATIONS = [n/3 for n in range(4)] # Four lights per side
def get_intensities(pos):
    # Scale intensity based on distance (quadratic dropoff)
    intens = [1-2*(l-pos)**2 for l in LIGHT_LOCATIONS]
    intens = [i if i >= 0 else 0 for i in intens]
    return intens

def tup_mult(tup, scale):
    return tuple(v * scale for v in tup)

def set_lights_instr(instrument, pos):
    res = [0] * 8
    intensity = get_intensities(pos)
    if instrument % 2 == 0: # Side A
        res[0:4] = intensity
    else:
        res[7:3:-1] = intensity
    lights = [tup_mult(INSTR_COLORS[instrument], i) for i in res]
    do_set_lights(lights)

pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0)
INSTR_COLORS = [(255, 100, 100), (100, 100, 255), (100, 255, 100), (255, 255, 90)]

ser = serial.Serial(SERIAL_PORT, 115200)
osc = udp_client.SimpleUDPClient("127.0.0.1", 4559) # Default OSC server location

cfg_instr_offset = 0
cfg_note_offset = 0

major_sixth = [0, 4, 7, 9]
chord_progression = [0, 5, 3, 4] # I - VI - IV - V

last_note = None
chord_mode = False
last_ch_button = 1

while True:
    str_data = str(ser.readline(), "ascii").strip()
    num_data = [int(i) for i in str_data.split(" ")]
    print(num_data)
    if (len(num_data) != 6): # Gracefully ignore -- sometimes first input is incomplete
        print("Expected 6 serial data inputs, skipping line")
        continue
    if (num_data[3]): # Config mode
        c = get_cfg(num_data[0], num_data[1])
        print(c)
        if c is not None:
            if c[0] == 0: # Instrument change setting
                cfg_instr_offset = 2 if c[1] > 0.5 else 0
            elif c[1] == 1: # Volume change setting
                cfg_note_offset = c[1] // 0.1
        last_note = None
        last_ch_button = 1
    else: # Instrumental mode
        if num_data[2] != last_ch_button and num_data[2]: # Debounce not necessary due to 10 Hz input rate
            chord_mode ^= True
        n = get_note(num_data[0], num_data[1])
        print(n)
        if n is not None:
            set_lights_instr(n[0]+cfg_instr_offset, n[2])
        if n is not None and last_note is not None and \
                n[1] != last_note[1]: # Valid note change

            # Buttons change the note (note all button inputs are normally 1)
            if not num_data[4]:
                    if not num_data[5]:
                        note_offset = 3
                    else:
                        note_offset = 1
            elif not num_data[5]:
                note_offset = 2
            else:
                note_offset = 0
            for nt in range_between(last_note[1], n[1], chord_mode):
                osc.send_message("/note", [n[0]+cfg_instr_offset, 70+cfg_note_offset+note_offset+nt, 0 if not chord_mode else nt+1])
        last_note = n
        last_ch_button = num_data[2]

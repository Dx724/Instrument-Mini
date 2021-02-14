import serial, time, math
from pythonosc import osc_message_builder
from pythonosc import udp_client

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
    return (instrument, sect)

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
def range_between(a, b): # From sector a to sector b
    if a < b: return range(a, b) # Sector 0 to Sector 1 plays "String" 0
    else: return range(b, a) # Sector 1 to Sector 0 plays "String" 0

ser = serial.Serial(SERIAL_PORT, 115200)
osc = udp_client.SimpleUDPClient("127.0.0.1", 4559) # Default OSC server location

cfg_instr_offset = 0
cfg_note_offset = 0

major_sixth = [0, 4, 3, 2]

last_note = None

while True:
    str_data = str(ser.readline(), "ascii").strip()
    num_data = [int(i) for i in str_data.split(" ")]
    print(num_data)
    assert len(num_data) == 6, "expecting 6 serial data inputs"
    if (num_data[3]): # Config mode
        c = get_cfg(num_data[0], num_data[1])
        print(c)
        if c is not None:
            if c[0] == 0: # Instrument change setting
                cfg_instr_offset = 2 if c[1] > 0.5 else 0
            elif c[1] == 1: # Volume change setting
                cfg_note_offset = c[1] // 0.1
        last_note = None
    else:
        n = get_note(num_data[0], num_data[1])
        print(n)
        if n is not None and last_note is not None and \
                n[1] != last_note[1]: # Valid note change
            for nt in range_between(last_note[1], n[1]):
                osc.send_message("/note", [n[0]+cfg_instr_offset, 70+cfg_note_offset+major_sixth[nt]])
        last_note = n

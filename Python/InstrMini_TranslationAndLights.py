import serial, time, math

# CONFIGURATION BEGIN
SERIAL_PORT = "COM4" # Serial port -- check device manager or ports listing
# Options below are purely for customization
DEAD_ZONE = 500 # Increase this to require larger joystick movements for sound
# CONFIGURATION END

ADC_RANGE = 4096
ADC_CENTER = ADC_RANGE // 2
NUM_NOTES = 4 # Notes per instrument

def to_angle(j_x, j_y):
    return math.atan2(j_y, j_x)

def get_note(joy_x, joy_y):
    joy_x -= ADC_CENTER
    joy_y -= ADC_CENTER
    if (joy_x ** 2 + joy_y ** 2) < DEAD_ZONE ** 2:
        return (-1, -1)
    note_angle = to_angle(joy_x, joy_y)
    instrument = int(note_angle > 0)
    note = abs(note_angle) // (math.pi / 4.0)
    return (instrument, note)

ser = serial.Serial(SERIAL_PORT, 115200)

while True:
    try:
        str_data = str(ser.readline(), "ascii").strip()
        num_data = [int(i) for i in str_data.split(" ")]
        print(num_data)
        print(get_note(num_data[0], num_data[1]))
    except Exception as e:
        print(e)
        break

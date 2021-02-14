import serial, time

# CONFIGURATION BEGIN
SERIAL_PORT = "COM4" # Serial port -- check device manager or ports listing
# CONFIGURATION END

ser = serial.Serial(SERIAL_PORT, 115200)

while True:
    try:
        str_data = str(ser.readline(), "ascii").strip()
        num_data = [int(i) for i in str_data.split(" ")]
        print(num_data)
        time.sleep(0.1)
    except Exception as e:
        print(e)
        break

import serial
import time

serial_speed = 115200
serial_port = 'COM3'

ser = serial.Serial(serial_port, serial_speed, timeout = 1)

for i in range(100):
    data = ser.readline()
    print(data)
    time.sleep(1)
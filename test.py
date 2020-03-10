import serial
import time

serial_speed = 115200
serial_port = '/dev/cu.usbmodem1411' #'/dev/tty.usbmodem1411' #'/dev/cu.usbmodem1411' #
ser = serial.Serial(serial_port, serial_speed, timeout = 1)

#for i in range(100):
while True:
    data = ser.readline()
    #print(data.decode())
    print(data.decode('utf-8'))
    #time.sleep(1)


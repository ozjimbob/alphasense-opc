#9600, 8, none, stop1, noflow

from __future__ import print_function
import serial
import time
import struct

serial_opts = {
    # built-in serial port is "COM1"
    # USB serial port is "COM4"
    "port": "/dev/ttyACM0",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "bytesize": serial.EIGHTBITS,
	"stopbits": serial.STOPBITS_ONE,
    "xonxoff": False,
	"timeout": 1
}


ser = serial.Serial(**serial_opts)
ser.open()

# Init
print("Init:")
ser.write(bytearray([0x5A,0x01]))
print(ser.read(3))
time.sleep(1)
ser.write(bytearray([0x5A,0x03]))
print(ser.read(9))
time.sleep(1)
ser.write(bytearray([0x5A,0x02,0x92,0x07]))
print(ser.read(2))
time.sleep(1)

# Turn fan off
def fanOff():
	ser.write(bytearray([0x61,0x03,0x01]))
	time.sleep(1)
	ser.read(3)

def fanOn():
	ser.write(bytearray([0x61,0x03,0x00]))
	time.sleep(1)
	ser.read(3)

def GetData():
	ser.write(bytearray([0x61,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32]))
	time.sleep(1)
	ans=bytearray(ser.read(14))
	print(ans)
	b1 = ans[2:6]
	b2 = ans[6:10]
	b3 = ans[10:14]
	c1=struct.unpack('f',bytes(b1))[0]
	c2=struct.unpack('f',bytes(b2))[0]
	c3=struct.unpack('f',bytes(b3))[0]
	return([c1,c2,c3])

print("Fan On:")
fanOn()

print("Opening Output File:")
f=open("out.csv",'w+')
print("Looping:")
for i in range(0,2400):
	print("Loop:"+str(i))
	t=GetData()
	print(str(t[0]) + "," + str(t[1]) + "," + str(t[2]), file=f)
	f.flush()
	time.sleep(5)
	
print("Closing:")

f.close()
fanOff()

ser.close()


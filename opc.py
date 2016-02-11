#9600, 8, none, stop1, noflow

from __future__ import print_function
import serial
import time
import struct
import datetime

# Init
def initOPC(ser):
	print("Init:")
	time.sleep(1)
	ser.write(bytearray([0x5A,0x01]))
	nl = ser.read(3)
	print(nl)
	time.sleep(.1)
	ser.write(bytearray([0x5A,0x03]))
	nl=ser.read(9)
	print(nl)
	time.sleep(.1)
	ser.write(bytearray([0x5A,0x02,0x92,0x07]))
	nl=ser.read(2)
	print(nl)
	time.sleep(.1)

# Turn fan and laser off
def fanOff(ser):
	ser.write(bytearray([0x61,0x03]))
	nl = ser.read(2)
	print(nl)
	time.sleep(.1)
	ser.write(bytearray([0x61,0x01]))
	nl = ser.read(2)
	print(nl)
	time.sleep(.1)

# Turn fan and laser on
def fanOn(ser):
        ser.write(bytearray([0x61,0x03]))
        nl = ser.read(2)
	print(nl)
        time.sleep(.1)
        ser.write(bytearray([0x61,0x00]))
        nl = ser.read(2)
	print(nl)
        time.sleep(.1)

def getHist(ser):
	ser.write(bytearray([0x61,0x30]))
	nl=ser.read(2)
	print(nl)
	time.sleep(.1)
	br = bytearray([0x61])
	for i in range(0,62):
		br.append(0x30)
	print(len(br))
	ser.write(br)
	ans=bytearray(ser.read(63))
	print(len(ans))
	print(ans[1:63])
	
# Retrieve data
def getData(ser):
	ser.write(bytearray([0x61,0x32]))
	nl=ser.read(2)
	print(nl)
	time.sleep(.1)
	ser.write(bytearray([0x61,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32]))
	ans=bytearray(ser.read(13))
	print(len(ans))
	print(ans[1:13])
	b1 = ans[1:5]
	b2 = ans[5:9]
	b3 = ans[9:13]
	c1=struct.unpack('f',bytes(b1))[0]
	c2=struct.unpack('f',bytes(b2))[0]
	c3=struct.unpack('f',bytes(b3))[0]
	return([c1,c2,c3])

if __name__ == "__main__":
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

	print("Init:")
	initOPC(ser)
	time.sleep(1)

	print("Fan Off:")
	fanOff(ser)
	time.sleep(5)
	
	print("Fan on:")
	fanOn(ser)
	time.sleep(5)	

	print("Opening Output File:")
	f=open("out.csv",'w+')
	print("Looping:")
	for i in range(0,400):
		print("Loop:"+str(i))
		#t=getData(ser)
		t=getData(ser)
		ts = time.time()
		tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print(tnow + "," + str(t[0]) + "," + str(t[1]) + "," + str(t[2]), file=f)
		print(tnow + "," + str(t[0]) + "," + str(t[1]) + "," + str(t[2]))
		f.flush()
		time.sleep(5)
	
	print("Closing:")

	f.close()
	fanOff(ser)

	ser.close()


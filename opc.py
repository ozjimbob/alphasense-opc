#9600, 8, none, stop1, noflow

from __future__ import print_function
import serial
import time
import struct
import datetime
import sys
import os.path

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

def combine_bytes(LSB, MSB):
	return (MSB << 8) | LSB

def getHist(ser):
	ser.write(bytearray([0x61,0x30]))
	nl=ser.read(2)
	print(nl)
	time.sleep(.1)
	br = bytearray([0x61])
	for i in range(0,62):
		br.append(0x30)
	ser.write(br)
	ans=bytearray(ser.read(1))
	ans=bytearray(ser.read(62))
	data={}
	data['Bin 0'] = combine_bytes(ans[0],ans[1])
	data['Bin 1'] = combine_bytes(ans[2],ans[3])
	data['Bin 2'] = combine_bytes(ans[4],ans[5])
	data['Bin 3'] = combine_bytes(ans[6],ans[7])
	data['Bin 4'] = combine_bytes(ans[8],ans[9])
	data['Bin 5'] = combine_bytes(ans[10],ans[11])
	data['Bin 6'] = combine_bytes(ans[12],ans[13])
	data['Bin 7'] = combine_bytes(ans[14],ans[15])
	data['Bin 8'] = combine_bytes(ans[16],ans[17])
	data['Bin 9'] = combine_bytes(ans[18],ans[19])
	data['Bin 10'] = combine_bytes(ans[20],ans[21])
	data['Bin 11'] = combine_bytes(ans[22],ans[23])
	data['Bin 12'] = combine_bytes(ans[24],ans[25])
	data['Bin 13'] = combine_bytes(ans[26],ans[27])
	data['Bin 14'] = combine_bytes(ans[28],ans[29])
	data['Bin 15'] = combine_bytes(ans[30],ans[30])
	data['period'] = struct.unpack('f',bytes(ans[44:48]))[0]
	data['pm1'] = struct.unpack('f',bytes(ans[50:54]))[0]
	data['pm2'] = struct.unpack('f',bytes(ans[54:58]))[0]
	data['pm10'] = struct.unpack('f',bytes(ans[58:]))[0]
	return(data)
	
# Retrieve data
def getData(ser):
	ser.write(bytearray([0x61,0x32]))
	nl=ser.read(2)
	time.sleep(.1)
	ser.write(bytearray([0x61,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32,0x32]))
	ans=bytearray(ser.read(13))
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

	ofile=sys.argv[1]

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
	if(not os.path.isfile(ofile)):
		f=open(ofile,'w+')
		print("time,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,period,pm1,pm2,pm10",file=f)
	else:
		f=open(ofile,'a')
	print("Looping:")
	for i in range(0,4320):
		t=getHist(ser)
		ts = time.time()
		tnow = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		data=t
		print(tnow + "," + str(data['Bin 0']) + ","  + str(data['Bin 1']) + ","  + str(data['Bin 2']) + ","  + str(data['Bin 3']) + ","  + str(data['Bin 4']) + ","  + str(data['Bin 5']) + ","  + str(data['Bin 6']) + ","  + str(data['Bin 7']) + ","  + str(data['Bin 8']) + ","  + str(data['Bin 9']) + ","  + str(data['Bin 10']) + ","  + str(data['Bin 11']) + ","  + str(data['Bin 12']) + ","  + str(data['Bin 13']) + ","  + str(data['Bin 14']) + ","  + str(data['Bin 15']) + ","  + str(data['period']) + ","  + str(data['pm1']) + ","  + str(data['pm2']) + ","  + str(data['pm10']) , file=f)
		print(tnow + "," + str(data['pm1']) + "," + str(data['period']) + "," + str(data['Bin 15']))
		f.flush()
		time.sleep(59)
	
	print("Closing:")

	f.close()
	fanOff(ser)

	ser.close()


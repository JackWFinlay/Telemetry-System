import RPi.GPIO as GPIO
import time
import sys

def bin2dec(string_num):
    return str(int(string_num, 2))

if len(sys.argv)==2:
	channel=int(sys.argv[1])
else:
	channel=7
#print str(channel)

data = []
threshold=6

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel,GPIO.OUT)
GPIO.output(channel,GPIO.HIGH)
time.sleep(0.025)
GPIO.output(channel,GPIO.LOW)
time.sleep(0.02)

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for i in range(0,1000):
    data.append(GPIO.input(channel))

bit_count = 0
tmp = 0
count = 0
HumidityBit = ""
TemperatureBit = ""
crc = ""
HStr = ""
TStr = ""

try:
	while data[count] == 1:
		tmp = 1
		count = count + 1
#	print "start:"+str(count)

	for i in range(0, 32):
		bit_count = 0

		while data[count] == 0:
			tmp = 1
			count = count + 1
#		print "    digit"+str(i)+" start:"+str(count)

		while data[count] == 1:
			bit_count = bit_count + 1
			count = count + 1
#		print "    digit"+str(i)+" end:"+str(count)

#		print str(i)+"):"+str(bit_count)
		if i>=0 and i<8:
			HStr = HStr + "-"
			HStr = HStr + str(bit_count)
		if i>=16 and i<24:
			TStr = TStr + "-"
			TStr = TStr + str(bit_count)
			
#		if bit_count > 3:
		if bit_count > threshold:
			if i>=0 and i<8:
				HumidityBit = HumidityBit + "1"
			if i>=16 and i<24:
				TemperatureBit = TemperatureBit + "1"
		else:
			if i>=0 and i<8:
				HumidityBit = HumidityBit + "0"
			if i>=16 and i<24:
				TemperatureBit = TemperatureBit + "0"

except:
	print "ERR_RANGE_hum_tem"
	GPIO.cleanup()
	exit(0)

if 0:
	print "H:"+HumidityBit
	print "T:"+TemperatureBit
	print "\n"
	print "h:"+HStr
	print "t:"+TStr


try:
	for i in range(0, 8):
		bit_count = 0

		while data[count] == 0:
			tmp = 1
			count = count + 1

		while data[count] == 1:
			bit_count = bit_count + 1
			count = count + 1

#		if bit_count > 3:
		if bit_count > threshold:
			crc = crc + "1"
		else:
			crc = crc + "0"
except:
	print "ERR_RANGE_crc"
	exit(0)

Humidity = bin2dec(HumidityBit)
Temperature = bin2dec(TemperatureBit)

H_value = int(Humidity) 
T_value = int(Temperature)

if T_value + H_value - int(bin2dec(crc)) == 0:
	print "Humidity:"+ Humidity +"%"
	print "Temperature:"+ Temperature +"C"
        exit(0) # Nagios status 'Normal'
else:
	print "ERR_CRC"
	exit(3) # Nagios status 'Unknown'

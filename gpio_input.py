#!/usr/bin/python
import RPi.GPIO as GPIO
import time
channel = 5

GPIO.setmode(GPIO.BOARD) # Set library to use board numbering rather than internal numbering of the SOC channels
GPIO.setup(channel, GPIO.IN) # Set up channel to use for input.


# while True:
time.sleep(1)
generatorStatus = GPIO.input(channel) # Read value of the GPIO channel. At this stage I believe 1 is standby, 0 running.
    
if (generatorStatus):
	GPIO.cleanup() # Release channel for next run of script.
        print "Reading status 1"
        exit(0) # Nagios status 'Normal'
else:
	GPIO.cleanup() # Release channel for next run of script.
	print "Reading status 0"
	exit(1) # Nagios status 'Warning'


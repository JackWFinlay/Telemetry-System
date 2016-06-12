#!/usr/bin/python

# Author: Jack Finlay 
# Gets the current status of the attached hardware device.
import RPi.GPIO as GPIO
import sys

channel = int(sys.argv[1]) # Set the first supplied argument as the channel.

GPIO.setmode(GPIO.BOARD) # Set library to use board numbering rather than internal numbering of the SOC channels
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set up channel to use for input. Bias the floating voltage towards zero.


# while True:
generatorStatus = GPIO.input(channel) # Read value of the GPIO channel. At this stage I believe 1 is standby, 0 running.
    
if (generatorStatus):
	GPIO.cleanup() # Release channel for next run of script.
    print "Reading status 1"
    exit(0) # Nagios status 'Normal'
    
else:
	GPIO.cleanup() # Release channel for next run of script.
	print "Reading status 0"
	exit(2) # Nagios status 'critical'


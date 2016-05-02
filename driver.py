#!/usr/bin/python
import RPi.GPIO as GPIO
from datetime import datetime

print GPIO.VERSION

channel = 8
pulseNormal = 5
pulseMin = 1
pulseTimeout = 10
pulseTimeoutMilliseconds = pulseTimeout * 1000

GPIO.setmode(GPIO.BOARD) # Set library to use board numbering rather than internal numbering of the SOC channels
GPIO.setup(channel, GPIO.IN) # Set up channel to use for input.

while (True):
    print "Waiting for initial edge."
    something = GPIO.wait_for_edge(channel, GPIO.RISING, timeout=pulseTimeoutMilliseconds) # Wait for High signal to start.
    timeStart = datetime.now() # Gets the current timestamp.
    print "Timeout or Rising edge detected: " + timeStart

    print "Waiting for pulse."
    something = GPIO.wait_for_edge(channel, GPIO.RISING, timeout=pulseTimeoutMilliseconds) # Wait for another pulse, timeout after timeout
    timePulse = datetime.now() # Gets the current timestamp so we can then work out the time difference.
    print "Timeout or Pulse detected: " + timePulse

    timeDelta = timePulse - timeStart
    print timeDelta

    if (timeDelta.seconds > pulseNormal):
        print "Pulse rate greater than normal."
        exit(1) # Nagios status 'Warning'
    elif (timeDelta.seconds < pulseNormal):
        print "Pulse rate less than normal."
        exit(1) # Nagios status 'Warning'
    elif (timeDelta.seconds > pulseTimeout):
        print "No pulse. Status Unknown"
        exit(3) # Nagios status 'Unknown'
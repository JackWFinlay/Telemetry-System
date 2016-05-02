#!/usr/bin/python
import RPi.GPIO as GPIO
import json
import time
from datetime import datetime

print GPIO.VERSION

with open('availabilityconfig.json') as config:
    data = json.load(config)

channel              = data["channel"] # The GPIO channel used for sensing the pulse.
pulseNormal          = data["pulseNormal"] # The normal setting for the pulse rate.
pulseMin             = data["pulseMin"] # The start of the range for timer.
pulseMax             = data["pulseMax"] # The end of the range for timer.
tolerance            = data["tolerance"] # tolerance for timer.

pulseMaxMilliseconds = pulseMax * 1000

print "Channel: "     + str(channel)
print "pulseNormal: " + str(pulseNormal)
print "pulseMin: "    + str(pulseMin)
print "pulseMax: "    + str(pulseMax)
print "tolerance: "  + str(tolerance)

GPIO.setmode(GPIO.BOARD) # Set library to use board numbering rather than internal numbering of the SOC channels
GPIO.setup(channel, GPIO.IN) # Set up channel to use for input.
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Bias the floating voltage to 0 when disconnected.

print "Waiting for initial edge."
something = GPIO.wait_for_edge(channel, GPIO.RISING)#, timeout=pulseMaxMilliseconds) # Wait for High signal to start.
timeStart = datetime.now() # Gets the current timestamp.
print "Timeout or Rising edge detected: " + str(timeStart)

print "Sleeping for " + str(pulseMin) + "seconds (pulseMin)."
time.sleep(pulseMin); # Sleep as no pulse is expected for pulseMin seconds. Also prevents switch bounce.

print "Waiting for pulse."
something = GPIO.wait_for_edge(channel, GPIO.RISING)#, timeout=pulseMaxMilliseconds) # Wait for another pulse, timeout after timeout
timePulse = datetime.now() # Gets the current timestamp so we can then work out the time difference.
print "Timeout or Pulse detected: " + str(timePulse)

timeDelta = timePulse - timeStart
print "Pulse rate: " + str(timeDelta)

if ((timeDelta.seconds > pulseNormal - tolerance) && (timeDelta.seconds < pulseNormal + tolerance)): # Check pulse time is normal and within tolerance
    print "Pulse rate normal."
    exit(0) # Nagios status 'Okay'.
elif (timeDelta.seconds < pulseMin):
    print "Pulse less than minimum. Error detected."
    exit(2) # Nagios status 'Critical'. Something is really wrong if pulse is faster than the range specified.
elif (timeDelta.seconds > pulseNormal):
    print "Pulse rate greater than normal."
    exit(1) # Nagios status 'Warning'
elif (timeDelta.seconds < pulseNormal):
    print "Pulse rate less than normal."
    exit(1) # Nagios status 'Warning'
elif (timeDelta.seconds > pulseMax):
    print "No pulse. Status Unknown"
    exit(3) # Nagios status 'Unknown' No pulse detected in usual range. Return unkown
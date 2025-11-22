"""
# Sensors.py
# Author: Arijit Sengupta
# Optimized for SteamBOT - only USS
"""

import utime
import math
from machine import Pin, ADC
from Log import *

class Sensor:
    """
    The top level sensor class - assume each sensor uses 
    at least one pin. We do not create the IO here because
    some sensors may use Analog inputs
    
    Parameters
    --------
    lowActive: set to True if the sensor gets low (or under threshold)
    when tripped. So an analog light sensor should normally get a high
    value but when covered, go low. So lowActive should be True
    
    A force sensor would be opposite - tripped when force gets high
    so lowActive should be False.

    Some of the digital sensors such as flame sensors, proximity sensors
    are lowActive, while others such as PIR sensors are highActive. Please
    check the sensor documentation for the correct value.
    """
    
    def __init__(self, name='Sensor', lowActive = True):
        self._lowActive = lowActive
        self._name = name

    def rawValue(self):
        Log.e(f"rawValue not implemented for {type(self).__name__} {self._name}")

    def tripped(self)->bool:
        Log.e(f"tripped not implemented for {type(self).__name__} {self._name}")
        return False

class UltrasonicSensor(Sensor):
    """
    A simple implementation of an ultrasonic sensor with digital IO
    pins for trigger and echo.
    
    While technically Ultrasonic sensor is not an analog sensor since it
    uses digital pins, it does have continuous data, so subclassing
    AnalogSensor makes more sense. But given AnalogSensor should only be
    used in ADC pins, it is better to subclass the Sensor superclass.
    
    Continuing to use the lowActive and threshold like AnalogSensor however.

    init by sending trigger, echo and optionally lowActive and threshold
    parameters. Threshold defaults to 10cm, and lowActive defaults to true
    so when distance is < 10cm, it will return true for tripped.
    """

    def __init__(self, *, trigger=0, echo=1, name='Ultrasonic', lowActive = True, threshold=10.0):
        super().__init__(name, lowActive)
        self._trigger = Pin(trigger, Pin.OUT)
        self._echo = Pin(echo, Pin.IN)
        self._threshold = threshold

    def rawValue(self):
        """ Return the distance in cm """
        return self.distance()
    
    def distance(self)->float:
        """ Get the distance of obstacle from the sensor in cm """
        
        self._trigger.off()
        utime.sleep_us(2)
        self._trigger.on()
        utime.sleep_us(5)
        self._trigger.off()
        while self._echo.value() == 0:
            signaloff = utime.ticks_us()
        while self._echo.value() == 1:
            signalon = utime.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return distance

    def tripped(self)->bool:
        """ sensor is tripped if distance is higher or lower than threshold """
        
        v = self.rawValue()
        if (self._lowActive and v < self._threshold) or (not self._lowActive and v > self._threshold):
            Log.i(f"UltrasonicSensor {self._name}: sensor tripped")
            return True
        else:
            return False

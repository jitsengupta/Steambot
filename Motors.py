"""
Motors.py - a class containing code to drive different types
of motors.
# Author: Arijit Sengupta

Optimized for SteamBOT - do not merge into
main branch.
"""

from machine import Pin, PWM
from time import sleep
from Log import *

class Motor:
    """
    A Motor superclass just to keep things together if we need to
    Currently simply stores the main pin (some motors take multiple pins)
    and a name for the motor.
    """
    
    def __init__(self, pin, name='Unnamed Motor'):
        self._pin = pin
        self._name = name
        
class CoolingFan(Motor):
    """
    A simple DC Motor that only needs a PWM line to control speed.
    Typically CPU cooling fans that come with 3 pins with an internal
    driver. Connect Red and Black to power, and data pin to any GPIO
    pin on the Pico.
    """
    def __init__(self, enable_pin = 0, name="Fan", min_duty=0, max_duty=65535):
        super().__init__(enable_pin, name)
        self.enable_pin = PWM(Pin(enable_pin))
        self.enable_pin.freq(1000)
        self.min_duty = min_duty
        self.max_duty = max_duty
    
    def run(self, speed):
        Log.i(f"Running fan {self._name} at speed {speed}")
        self.speed = speed
        self.enable_pin.duty_u16(self.duty_cycle(self.speed))
        
    def stop(self):
        Log.i(f"Stopping fan {self._name}")
        self.run(0)
        
    def duty_cycle(self, speed):
        if speed <= 0 or speed > 100:
            duty_cycle = 0
        else:
            duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty) * (speed / 100))
        return duty_cycle
    
# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-dc-motor-micropython/

class DCMotor(CoolingFan):
    """
    Implements a standard DC motor with 2 pins that can be controlled
    for bidirectional controllable velocities. Typically the enable_pin is used for
    PWM control of the speed, and the forward_pin and backward_pin are used for
    controlling the direction of the motor.

    Direction can also be controlled using a single pin by using the enable_pin
    for PWM and setting the forward_pin to 1 or 0 to control direction. In this case,
    use None for backward_pin.

    Needs to use a driver chip like L293N or L298N to function correctly.
    """
    
    def __init__(self, enable_pin = 0, name="DCMotor", forward_pin = 1, backward_pin=None, min_duty=15000, max_duty=65535):
        super().__init__(enable_pin, name, min_duty, max_duty)
        self.pin1 = Pin(forward_pin, Pin.OUT)
        if backward_pin is None:
            self.pin2 = None
        else:
            self.pin2 = Pin(backward_pin, Pin.OUT)

    def forward(self, speed=100):
        """ Spin motor forward at a percent speed (max:100)"""
        
        Log.i(f"Moving {self._name} forward at speed {speed}")
        self.speed = speed
        self.pin1.value(1)
        if self.pin2 is not None:
            self.pin2.value(0)
        self.enable_pin.duty_u16(self.duty_cycle(self.speed))

    def backwards(self, speed=100):
        """ Spin motor backwards at a percent speed (max:100) """
        
        Log.i(f"Moving {self._name} backwards at speed {speed}")
        self.speed = speed
        self.pin1.value(0)
        if self.pin2 is not None:
            self.pin2.value(1)
        self.enable_pin.duty_u16(self.duty_cycle(self.speed))

    def stop(self):
        """ Stop spinning the motor """
        
        Log.i(f"Stopping {self._name}")
        self.enable_pin.duty_u16(0)
        self.pin1.value(0)
        if self.pin2 is not None:
            self.pin2.value(0)

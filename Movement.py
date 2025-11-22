"""
Movement.py - Class for vehicle movement
Based on PicoLibrary Motor class
Written for the SteamBOT
"""

from Motors import *
import time

rightpwm = Pin(5, Pin.OUT)   # D1
leftpwm = Pin(4, Pin.OUT)   # D2
rightd = Pin(0, Pin.OUT)   # D3
leftd = Pin(2, Pin.OUT)   # D4

class Movement():
    """
    Movement class - move the bot forward, backward, left, right and stop
    """
    
    def __init__(self, lp=leftpwm, ld=leftd, rp=rightpwm, rd=rightd, lflip=False, rflip=True):
        """
        Initialize the movement
        Motors in SteamBOT has a single direction pin
        and a single pwm pin for speed control. Since
        the motors are mirrored, they need to spin
        in different directions
        """
        
        self.leftMotor = DCMotor(enable_pin=lp, forward_pin=ld, name="left")
        self.rightMotor = DCMotor(enable_pin=rp, forward_pin=rd, name="right")
        self._leftFlip = lflip
        self._rightFlip = rflip
            
    def forward(self, speed=100):
        """
        Move SteamBOT forward
        """
        
        if self._leftFlip:
            self.leftMotor.backwards(speed)
        else:
            self.leftMotor.forward(speed)
        if self._rightFlip:
            self.rightMotor.backwards(speed)
        else:
            self.rightMotor.forward(speed)
            
    def backward(self, speed=100):
        """
        Move SteamBOT backward
        """
        
        if self._leftFlip:
            self.leftMotor.forward(speed)
        else:
            self.leftMotor.backwards(speed)
        if self._rightFlip:
            self.rightMotor.forward(speed)
        else:
            self.rightMotor.backwards(speed)
            
    def left(self, speed=100):
        """
        Turn steambot left - stop the left motor
        spin the right motor forward
        """
        
        self.leftMotor.stop()
        if self._rightFlip:
            self.rightMotor.backwards(speed)
        else:
            self.rightMotor.forward(speed)

    def right(self, speed=100):
        """
        Turn steambot right - stop the right motor
        spin the left motor forward
        """
        
        self.rightMotor.stop()
        if self._leftFlip:
            self.leftMotor.backwards(speed)
        else:
            self.leftMotor.forward(speed)

    def stop(self):
        """
        Stop the SteamBOT
        """
        
        self.leftMotor.stop()
        self.rightMotor.stop()
        

if __name__ == '__main__':
    
    v = Movement()
    v.forward(100)
    time.sleep(0.5)
    v.stop()

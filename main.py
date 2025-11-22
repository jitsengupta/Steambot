from Net import *
from Motors import *
import time

rightpwm = Pin(5, Pin.OUT)   # D1
leftpwm = Pin(4, Pin.OUT)   # D2
rightd = Pin(0, Pin.OUT)   # D3
leftd = Pin(2, Pin.OUT)   # D4

class Vehicle(WebServer):
    
    def __init__(self, lp, ld, rp, rd, lflip, rflip):
        self.leftMotor = DCMotor(enable_pin=lp, forward_pin=ld, name="left")
        self.rightMotor = DCMotor(enable_pin=rp, forward_pin=rd, name="right")
        self._leftFlip = lflip
        self._rightFlip = rflip
        self._net = Net()
        self._net.startAccessPoint("PicoAP", "micropythoN")
        Log.i(self._net.getAccessPointInfo())
        super().__init__(self._net)
        
    def generate_html(self, params = None):
        html = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MicroPython Steambot</title>
            <link rel="icon" href="data:;base64,=">
            </head>
            <body>
            <h1>Simple SteamBot</h1>
            <pre>{self._net.getStatusString()}</pre>
            <pre>Params: {params}</pre>"""
        
        movement = None
        if 'action' in params:
            movement = params['action']
            
        if movement:
            if movement == 'forward':
                self.forward()
            elif movement == 'backward':
                self.backward()
            elif movement == 'left':
                self.left()
            elif movement == 'right':
                self.right()
            html = html + f"<p style='color:green'>Vehicle is moving {movement}.</p>"
        else:
            self.stop()
            html = html + "<p style='color:red'>Vehicle is stopped.</p>"
            
        html = html + """
        <p>&nbsp;&nbsp;&nbsp;  ^^^^^^  <a href='/?action=forward'>Forward</a>  ^^^^^^ </p>
        <p>&lt;-- <a href='/?action=left'>Left</a> &nbsp; | <a href='/'>STOP</a> |  &nbsp;  <a href='/?action=right'>Right</a> --&gt;</p>
        <p>&nbsp;&nbsp;&nbsp;  vvvvv  <a href='/?action=backward'>Backward</a>  vvvvv </p>
        </body></html>"""
        
        return html
    
    def forward(self, speed=100):
        if self._leftFlip:
            self.leftMotor.backwards(speed)
        else:
            self.leftMotor.forward(speed)
        if self._rightFlip:
            self.rightMotor.backwards(speed)
        else:
            self.rightMotor.forward(speed)
            
    def backward(self, speed=100):
        if self._leftFlip:
            self.leftMotor.forward(speed)
        else:
            self.leftMotor.backwards(speed)
        if self._rightFlip:
            self.rightMotor.forward(speed)
        else:
            self.rightMotor.backwards(speed)
            
    def left(self, speed=100):
        self.leftMotor.stop()
        if self._rightFlip:
            self.rightMotor.backwards(speed)
        else:
            self.rightMotor.forward(speed)

    def right(self, speed=100):
        self.rightMotor.stop()
        if self._leftFlip:
            self.leftMotor.backwards(speed)
        else:
            self.leftMotor.forward(speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
        

if __name__ == '__main__':
    
    v = Vehicle(leftpwm, leftd, rightpwm, rightd, False, True)
    
    v.serveUI()        

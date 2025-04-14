import RPi.GPIO as io
import time
from servo import Servo

def servo_control():
    io.output(Servo.vcc, io.HIGH)
    io.output(Servo.grd, io.LOW)
    for i in range(0,181):  
        sig=(i/18)+2  
        Servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)  
    for i in range(180,-1,-1):  
        sig=(i/18)+2  
        Servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)
    Servo.pwm.stop()
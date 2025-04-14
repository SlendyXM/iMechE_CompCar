import RPi.GPIO as io
import time
from servo import Servo

servo = Servo()

def servo_control():    
    for i in range(0,181):  
        sig=(i/18)+2  
        servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)  
    for i in range(180,-1,-1):  
        sig=(i/18)+2  
        servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)
    servo.pwm.stop()
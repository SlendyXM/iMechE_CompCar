import RPi.GPIO as io
import time
from plunger.servo import Servo

servo = Servo()

def servo_control():    
    '''for i in range(0,181):  
        sig=(i/18)+2  
        servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)  
    for i in range(180,-1,-1):  
        sig=(i/18)+2  
        servo.pwm.ChangeDutyCycle(sig)  
        time.sleep(0.03)
    servo.pwm.stop()'''
    for i in range(0,3):
        servo.pwm.ChangeDutyCycle(2.0) # rotate to 0 degrees
        time.sleep(0.5)
        servo.pwm.ChangeDutyCycle(12.0) # rotate to 180 degrees
        time.sleep(0.5)
        servo.pwm.ChangeDutyCycle(7.0) # rotate to 90 degrees
        time.sleep(0.5)
    servo.pwm.ChangeDutyCycle(0)
    servo.pwm.stop()
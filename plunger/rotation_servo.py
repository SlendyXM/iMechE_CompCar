import RPi.GPIO as io
import time
from plunger.servo import Servo

servo = Servo()

def servo_control():    
    servo.pwm.ChangeDutyCycle(6.99) # Let plunger fall
    time.sleep(0.8)
    servo.pwm.ChangeDutyCycle(9.49)
    time.sleep(0.8)
    servo.pwm.ChangeDutyCycle(0)
    servo.pwm.stop()

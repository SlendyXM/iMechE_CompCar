import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def rotate_anticlockwise(speed,duration):
	MotorA.forward()
	MotorB.forward()
	MotorC.backward()
	MotorD.backward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Rotating anticlockwise at {speed}% speed for {duration} seconds")
	time.sleep(duration)
import time
from ..mA import MotorA
from ..mD import MotorD

def backward_lateral_clockwise(speed,duration):
	MotorA.backward()
	MotorD.forward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
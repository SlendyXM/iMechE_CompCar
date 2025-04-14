import time
from ..mA import MotorA
from ..mD import MotorD

def backward_lateral_anticlockwise(speed,duration):
	MotorA.forward()
	MotorD.backward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to right at {speed}% speed for {duration} seconds")
	time.sleep(duration)
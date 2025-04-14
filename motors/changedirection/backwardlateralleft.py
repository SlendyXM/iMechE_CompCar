import time
from ..mA import MotorA
from ..mD import MotorD

motorA = MotorA()
motorD = MotorD()

def backward_lateral_clockwise(speed,duration):
	motorA.backward()
	motorD.backward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
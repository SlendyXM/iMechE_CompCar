import time
from ..mA import MotorA
from ..mD import MotorD

motorA = MotorA()
motorD = MotorD()

def backward_lateral_anticlockwise(speed,duration):
	motorA.forward()
	motorD.forward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to right at {speed}% speed for {duration} seconds")
	time.sleep(duration)
from ..mA import MotorA
from ..mD import MotorD

motorA = MotorA()
motorD = MotorD()

def backward_lateral_clockwise(speed):
	motorA.forward()
	motorD.backward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to left at {speed}% speed")
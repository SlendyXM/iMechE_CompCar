from ..mA import MotorA
from ..mD import MotorD

motorA = MotorA()
motorD = MotorD()

def backward_lateral_anticlockwise(speed):
	motorA.backward()
	motorD.forward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Changing backward direction to right at {speed}% speed")
	
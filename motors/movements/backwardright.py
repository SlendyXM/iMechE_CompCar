from ..mB import MotorB
from ..mD import MotorD

motorB = MotorB()
motorD = MotorD()

def backwardright(speed):
	motorB.backward()
	motorD.backward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving backward to the right at {speed}% speed")
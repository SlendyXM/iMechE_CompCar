from ..mB import MotorB
from ..mD import MotorD

motorB = MotorB()
motorD = MotorD()

def forwardleft(speed):
	motorB.forward()
	motorD.forward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving forward to the left at {speed}% speed")
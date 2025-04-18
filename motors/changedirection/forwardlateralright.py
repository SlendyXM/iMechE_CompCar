from ..mB import MotorB
from ..mC import MotorC

motorB = MotorB()
motorC = MotorC()

def forward_lateral_clockwise(speed):
	motorB.forward()
	motorC.backward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to right at {speed}% speed")
	
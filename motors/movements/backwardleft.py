from ..mA import MotorA
from ..mC import MotorC

motorA = MotorA()
motorC = MotorC()

def backwardleft(speed):
	motorA.backward()
	motorC.backward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Moving backward to the left at {speed}% speed")
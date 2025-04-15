import time
from ..mB import MotorB
from ..mC import MotorC

motorB = MotorB()
motorC = MotorC()

def forward_lateral_anticlockwise(speed,duration):
	motorB.backward()
	motorC.forward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
import time
from ..mB import MotorB
from ..mC import MotorC

motorB = MotorB()
motorC = MotorC()

def forward_lateral_clockwise(speed,duration):
	motorB.forward()
	motorC.forward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to right at {speed}% speed for {duration} seconds")
	time.sleep(duration)
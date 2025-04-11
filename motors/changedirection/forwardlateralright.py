import time
from ..mB import MotorB
from ..mC import MotorC

def forward_lateral_clockwise(speed,duration):
	MotorB.forward()
	MotorC.backward()
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to right at {speed}% speed for {duration} seconds")
	time.sleep(duration)
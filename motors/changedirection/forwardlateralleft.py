import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def forward_lateral_anticlockwise(speed,duration):
	MotorB.backward()
	MotorC.forward()
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
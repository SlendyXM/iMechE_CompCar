import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorB = MotorB()
motorC = MotorC()

def forward_lateral_anticlockwise(speed,duration):
	motorB.backward()
	motorC.forward()
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Changing forward direction to left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
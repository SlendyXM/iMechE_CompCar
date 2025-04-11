import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def move_left(speed,duration):
	MotorA.forward()
	MotorB.backward()
	MotorC.forward()
	MotorD.backward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
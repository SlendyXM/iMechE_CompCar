import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def move_right(speed,duration):
	MotorA.backward()
	MotorB.forward()
	MotorC.backward()
	MotorD.forward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving right at {speed}% speed for {duration} seconds")
	time.sleep(duration)
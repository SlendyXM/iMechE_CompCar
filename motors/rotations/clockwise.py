import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def rotate_clockwise(speed,duration):
	MotorA.backward()
	MotorB.backward()
	MotorC.forward()
	MotorD.forward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Rotating clockwise at {speed}% speed for {duration} seconds")
	time.sleep(duration)
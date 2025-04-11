import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def move_forward(speed,duration):
	MotorA.forward()
	MotorB.forward()
	MotorC.forward()
	MotorD.forward()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving forward at {speed}% speed for {duration} seconds")
	time.sleep(duration)
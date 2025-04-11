import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

def stop(speed,duration):
	MotorA.stop()
	MotorB.stop()
	MotorC.stop()
	MotorD.stop()
	MotorA.pwm.ChangeDutyCycle(speed)
	MotorB.pwm.ChangeDutyCycle(speed)
	MotorC.pwm.ChangeDutyCycle(speed)
	MotorD.pwm.ChangeDutyCycle(speed)
	print(f"Stopping for {duration} seconds")
	time.sleep(duration)
import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorA = MotorA()
motorB = MotorB()
motorC = MotorC()
motorD = MotorD()

def stop(speed,duration):
	motorA.stop()
	motorB.stop()
	motorC.stop()
	motorD.stop()
	motorA.pwm.ChangeDutyCycle(speed)
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Stopping for {duration} seconds")
	time.sleep(duration)
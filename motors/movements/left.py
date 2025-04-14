import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorA = MotorA()
motorB = MotorB()
motorC = MotorC()
motorD = MotorD()

def move_left(speed,duration):
	motorA.forward()
	motorB.backward()
	motorC.backward()
	motorD.forward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving left at {speed}% speed for {duration} seconds")
	time.sleep(duration)
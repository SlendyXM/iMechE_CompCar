import time
from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorA = MotorA()
motorB = MotorB()
motorC = MotorC()
motorD = MotorD()

def rotate_anticlockwise(speed,duration):
	motorA.forward()
	motorB.forward()
	motorC.backward()
	motorD.backward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Rotating anticlockwise at {speed}% speed for {duration} seconds")
	time.sleep(duration)
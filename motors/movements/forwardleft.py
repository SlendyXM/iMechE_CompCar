from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorA = MotorA()
motorB = MotorB()
motorC = MotorC()
motorD = MotorD()

def forwardleft(speed):
	motorA.forward()
	motorB.stop()
	motorC.forward()
	motorD.stop()
	motorA.pwm.ChangeDutyCycle(speed)
	motorB.pwm.ChangeDutyCycle(0)
	motorC.pwm.ChangeDutyCycle(speed)
	motorD.pwm.ChangeDutyCycle(0)
	print(f"Moving forward to the left at {speed}% speed")

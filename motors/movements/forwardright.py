from ..mA import MotorA
from ..mB import MotorB
from ..mC import MotorC
from ..mD import MotorD

motorA = MotorA()
motorB = MotorB()
motorC = MotorC()
motorD = MotorD()

def forwardright(speed):
	#motorA.stop()
	motorB.forward()
	#motorC.stop()
	motorD.forward()
	motorA.pwm.ChangeDutyCycle(0)
	motorB.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(0)
	motorD.pwm.ChangeDutyCycle(speed)
	print(f"Moving forward to the right at {speed}% speed")

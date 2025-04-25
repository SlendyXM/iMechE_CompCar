from ..mA import MotorA
from ..mC import MotorC

motorA = MotorA()
motorC = MotorC()

def forwardright(speed):
	motorA.forward()
	motorC.forward()
	motorA.pwm.ChangeDutyCycle(speed)
	motorC.pwm.ChangeDutyCycle(speed)
	print(f"Moving forward to the right at {speed}% speed")
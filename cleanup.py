import RPi.GPIO as io

stby_pin						= [3]
motor_a_pins					= [11, 13, 15]
motor_b_pins					= [19, 21, 23]
motor_c_pins					= [22, 24, 26]
motor_d_pins					= [36, 38, 40]
plunger_pin						= [8]
color_sensor_a_pins				= [29, 31, 32, 33, 35, 37]
all_pins = (stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + 
            plunger_pin + color_sensor_a_pins)
io.cleanup([all_pins])
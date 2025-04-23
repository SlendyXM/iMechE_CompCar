import RPi.GPIO as io

io.setmode(io.BOARD)
io.setup(3, io.OUT)  # STBY
io.setup(12, io.OUT)
io.setup(16, io.OUT)
io.output(3, io.HIGH)  # enable board


while True:
    io.output(12, io.HIGH)
    io.output(16, io.LOW)
    io.output(12, io.LOW)
    io.output(16, io.HIGH)
    
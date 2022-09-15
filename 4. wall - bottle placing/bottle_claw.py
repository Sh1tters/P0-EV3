#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

ev3 = EV3Brick()


left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
touch = TouchSensor(Port.S2)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)


# Opening the claw, in order to be ready to grab the bottle.
claw_motor.run_time(-1000,2500, wait = True)

# When the touch sensor is pressed by the bottle, this loop will begin.
# The robot will stop movement, close the claw, then move. It will then release the bottle,
# back up, and close the claw to our chosen default position.
while True:
    robot.drive(50, 0)
    if touch.pressed():
        robot.stop()
        claw_motor.run_until_stalled(1000, then = Stop.HOLD, duty_limit = 30)
        robot.straight(-500)
        robot.straight(500)
        claw_motor.run_until_stalled(-1000,then = Stop.COAST, duty_limit = 30)
        robot.straight(-150)
        claw_motor.run_time(1000,2500, wait = True)
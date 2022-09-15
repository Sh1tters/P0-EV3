#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font
from helper_classes import LineFollower

ev3 = EV3Brick()

lf = LineFollower()

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
touch = TouchSensor(Port.S2)
color_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)


# When the robot meets the 4. wall, it will let go of the bottle, back up, 
# set the claw into driving position, turn 135 degrees to the left.

claw_motor.run_until_stalled(-1000,then = Stop.COAST, duty_limit = 30)
robot.straight(-200)
claw_motor.run_time(1000,2500, wait = True)
robot.turn(-135)

# The robot will now drive until it finds the path again.

while True:
    if color_sensor.reflection() == lf.isOffPath():
        robot.run(100, 0)
    if color_sensor.reflection() == lf.isOnPath():
        robot.straight(35)
        robot.turn(45)
        break

# Now the robot will begin linefollowing until the next wall.
lf.run()


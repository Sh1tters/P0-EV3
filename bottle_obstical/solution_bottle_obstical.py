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


left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
claw_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

color_sensor = ColorSensor(Port.S3)
lf = LineFollower


# Outline for the protocol for avoiding the 2 bottles.
# It is assumed that the robot is running the linefollower protocol, and therefore
# will stop linefollowing when encountering the wall.
# The following it to begin, when the robot encounters the wall.

# First the robot will turn 45 degrees to the right, since the left is too close to another path.
robot.turn(45)

# Then the robot will drive so that it is parallel with the bottle.
# By my estimate, the distance ought to be 30 cm divided by cos(45 degrees) = approx. 42,5 cm.
robot.straight(425)

# Now the robot will do a 90 degree turn to the left, 
# and drive until it the color sensor reads a value = IsOnPath.

robot.turn(-90)

while True:
    if color_sensor.reflection() == lf.isOffPath():
        robot.run(100, 0)
    if color_sensor.reflection() == lf.isOnPath():
        robot.stop()
        break

lf.run()


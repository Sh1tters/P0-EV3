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



# First, the robot has to make a left turn. The more precise we can make it, the better,
# as we want the robot to face the bottle directly, when having performed the turn.
# This is due to the touch sensor.

# I have chosen to make a 45 degree turn, then have the robot drive 2 cm.
robot.turn(45)
robot.straight(20)

# Then is will drive until it finds the path.
while True:
    if color_sensor.reflection() == lf.isOffPath():
        robot.run(50, 0)
    if color_sensor.reflection() == lf.isOnPath():
        robot.straight(35) # When it finds the path, it will drive 2,5 cm divided by cos(45 degrees) = 3,5 cm.
                            # This way, it should be in the middle of the path.
        robot.turn(45)

        # It will now open the claw.
        claw_motor.run_time(-1000,2500, wait = True)
        break

# Now it will drive, until it meets the bottle.
while True:
    robot.drive(50, 0)
    if touch.pressed():
        robot.stop()
        claw_motor.run_until_stalled(1000, then = Stop.HOLD, duty_limit = 30)
        break

# At this point, the robot has grabbed the bottle. Now it will drive until it finds the 4. wall.

while True:
    if color_sensor.reflection() != lf.isOnWall():
        robot.run(50, 0)
    if color_sensor.reflection() == lf.isOnWall():
        robot.stop()
        break






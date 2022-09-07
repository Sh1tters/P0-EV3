#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

from settings import PATH_VALUE, WALL_VALUE, ACCEPTED_DEVIANCE, TURN_ANGLE, DRIVE_SPEED

from helper_classes import LineFollower

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A, Direction.CLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Make and Run Line Follower
lf = LineFollower(robot, line_sensor, PATH_VALUE, WALL_VALUE, ACCEPTED_DEVIANCE, TURN_ANGLE, DRIVE_SPEED)
lf.run()
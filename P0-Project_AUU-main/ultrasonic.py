#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from settings import (PATH_VALUE,
                      WALL_VALUE,
                      ACCEPTED_DEVIANCE,
                      TURN_ANGLE,
                      DRIVE_SPEED)

from helper_classes import LineFollower, Calibration

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)
claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
touch_sensor = TouchSensor(Port.S2)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=68.8, axle_track=120)

# Make Line Follower
lf = LineFollower(ev3, robot, line_sensor, PATH_VALUE, WALL_VALUE,
                  ACCEPTED_DEVIANCE, TURN_ANGLE, DRIVE_SPEED)

# Make Calibration

ev3.screen.clear()
ev3.screen.print(ultrasonic_sensor.distance())
wait(100)


while True:
    if ultrasonic_sensor.distance() > 30:
        ev3.screen.print(ultrasonic_sensor.distance())
        robot.drive(-50,0)
    else:
        ev3.screen.print(ultrasonic_sensor.distance())
        robot.stop()
        break
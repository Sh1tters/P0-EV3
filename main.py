#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from helper_classes import LineFollower, SettingsManager

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A, Direction.CLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Make settingsManager
sm = SettingsManager()
if not sm.loadSettings():
    ev3.screen.print("Settings not loaded... stopping")
    wait(10000)
    exit(1)

path_value = sm.getSetting("path_value")
accepted_deviance = sm.getSetting("accepted_deviance")
turn_angle = sm.getSetting("turn_angle")
drive_speed = sm.getSetting("drive_speed")

# Make Line Follower
lf = LineFollower(robot, line_sensor, path_value, accepted_deviance, turn_angle, drive_speed)

# Make Calibration
path_value = lf.calibrate()
lf.path_value = path_value
sm.setSetting("path_value", path_value)

# Run the line follower
lf.run()
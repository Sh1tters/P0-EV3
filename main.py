#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A, Direction.CLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Configure the path value measurements.
PATH_RANGE = 30 # Sensor Reflection Value
PATH_END_RANGE = 18 # Sensor Reflection Value

# Calculate the threshold
BLACK = 28
WHITE = 50
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 20 millimeters per second.
DRIVE_SPEED = 30

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2


class LineFollower:
    robot, pv, wv, ov, ta, lr = None
    def __init__(self, robot: DriveBase, pv: int, wv: int, ov: int, ta: int):
        #pv path value
        #wv wall value
        #off value
        #turn angle

        self.robot = robot
        self.pv = pv
        self.wv = wv
        self.ov = ov
        self.ta = ta

    def isOnPath(self) -> bool:
        return PATH_RANGE + 15 > line_sensor.reflection() > PATH_RANGE - 8

    def isOnWall(self) -> bool:
        return PATH_END_RANGE + 4 > line_sensor.reflection() > PATH_END_RANGE - 3

    def isOffPath(self) -> bool:
        return not self.isOnPath() and not self.isOnWall()

    def autocorrect_Path(self) -> None:
        ev3.screen.print('Starting auto correct path..')
        #TODO: MAKE IT WORK
        robot.stop()

        sm = 1
        d = 1
        while self.isOffPath() and sm * self.ta > 90:
            ba = 1
            if d < 0:
                ba = 2
            
            robot.turn(self.ta * sm * d * ba)

            if self.isOnPath():
                break

            if d < 0:
                sm+= 1
            d*=1

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
WALL_RANGE = 18 # Sensor Reflection Value
OFF_RANGE = 54 # Sensor Reflection Value

# Calculate the threshold
BLACK = 28
WHITE = 50
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 20 millimeters per second.
DRIVE_SPEED = 30


class LineFollower:
    robot, pv, wv, ov, ta, lr, ds = None
    def __init__(self, robot: DriveBase, pv: int, wv: int, ov: int, ta: int, ds: int):

        self.robot = robot
        self.pv = pv # path value
        self.wv = wv # wall value
        self.ov = ov # off value
        self.ta = ta # turn angle
        self.ds = ds # drive speed
        self.shut_down = False # shut down signal

    def isOnPath(self) -> bool:
        return self.pv + 15 > line_sensor.reflection() > self.pv - 8

    def isOnWall(self) -> bool:
        return self.wv + 4 > line_sensor.reflection() > self.wv - 3

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

    def adjust_lane(self):
        print('Adjusting to lane...')
    

    def run(self):

        # Configure robot settings
        robot.speed = self.speed


        # Deal with PID algorithm values - https://thecodingfun.com/2020/06/16/lego-mindstorms-ev3-pid-line-follower-code-by-using-micropython-2-0/
        Kp = 4.2 # Represents Proportional
        Ki = 0.008 # Represents Integral, which calculates the historically accumulated error
        Kd = 0.01 # Represents Derivative, which forecasts the future error based on the past error
        last_error = 0
        integral = 0
        derivative = 0

        # PID Algorithm combines three parts and assing factors Kp, Ki and Kd
        # to each of them and calculates the value of Turn, which will be added/subtracted

        # Main class loop
        while not self.shut_down:
            
            if self.isOffPath():
                self.autocorrect_Path()
            # Deal with wall cps
            elif self.isOnWall():

                robot.stop()
                # start challenge protocols
            else:
                
                error = line_sensor().reflection() - threshold
                integral = integral + error
                derivative = error - last_error

                turn_rate = Kp * error + Ki * integral + Kd * derivative
                left_motor(self.ds + turn_rate)
                right_motor(self.ds - turn_rate)

                wait(10)
            
            





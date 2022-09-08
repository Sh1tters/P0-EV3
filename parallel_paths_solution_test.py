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


# 7. wall - solution for parallel paths.
# Contains changing path twice on the left side of the robot.



robot.straight(200)
robot.turn(-90)

n = 0
while True:
    
    if n == 0:
        robot.drive(50,0)
        if line_sensor.reflection() > 30: #== lf.isOffPath():
            n += 1
            ev3.screen.print(n)
            robot.drive(50,0)

    
    if n == 1:
        robot.drive(50,0)
        if line_sensor.reflection() < 30: #== lf.isOnPath():
            n += 1
            ev3.screen.print(n)
            robot.drive(50,0)

    if n == 2:
        if line_sensor.reflection() > 30: #== lf.isOffPath():
            n += 1
            ev3.screen.print(n)
            robot.drive(50,0)

    if n == 3:
        if line_sensor.reflection() < 30:
            n += 1
            ev3.screen.print(n)
            robot.straight(70)
            robot.turn(90)
            break

lf.run()


                        
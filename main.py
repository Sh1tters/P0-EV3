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

# After first wall, LineFollower loop will break and
# begin on the following solution for the broken path.
robot.turn(45)
robot.straight(100)
while True:
    #if line_sensor.reflection() > lf.path_value
    if line_sensor.reflection() > 30:
        robot.drive(100, 0)
    #if line_sensor.reflection() < lf.path_value
    if line_sensor.reflection() < 30:
        robot.straight(70)
        robot.turn(-45)
        break

# Begin LineFollower again, once it finds the new path.
lf.run() 

# 2. wall - solution for the 2. broken path.
robot.turn(-45)
robot.straight(100)
while True: 
    if line_sensor.reflection() > 30:
        robot.drive(100, 0)
    if line_sensor.reflection() < 30:
        robot.straight(70)
        robot.turn(45)
        break

# Begin LineFollower again, once it finds the new line.
lf.run()

# 3. wall - solution for bottle-pickup.
# Contains a right turn and picking up bottle.


# 4. wall - solution for bottle-placing.
# Contains placing the bottle again and returning to the original path.


# 5. wall - left turn onto seesaw path.


# 6. wall - solution for seesaw.
# Contains crossing the seesaw and another left turn.


# 7. wall - solution for parallel paths.
# Contains change path twice on the left side of the robot.


# 8. wall - left turn onto bulls-eye path.


# 9. wall - solution for bulls-eye.
# Contains following the outer ring, location bottle,
# picking up bottle, and placing the bottle as close to the middle as possible.


# 10. wall - solution for avoiding bottle.


# 11. wall - solution for the tunnel.
# Contains 45 degree left turn, forward motion, a 90 degree right turn,
# forward motion, a 45 degree left turn, and finding the path again.


# 12. wall - solution for avoiding bottle.


# 13. wall - solution for landing zone.


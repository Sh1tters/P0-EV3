#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase

from settings import (PATH_VALUE,
                      WALL_VALUE,
                      ACCEPTED_DEVIANCE,
                      TURN_ANGLE,
                      DRIVE_SPEED)

from helper_classes import LineFollower, Calibration

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A, Direction.CLOCKWISE)
right_motor = Motor(Port.D, Direction.CLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)
claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
touch_sensor = TouchSensor(Port.S2)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Make Line Follower
lf = LineFollower(robot, line_sensor, PATH_VALUE, WALL_VALUE,
                  ACCEPTED_DEVIANCE, TURN_ANGLE, DRIVE_SPEED)

# Make Calibration
cal = Calibration(robot, line_sensor, lf)
cal.run()

lf.run()

# After first wall, LineFollower loop will break and
# begin on the following solution for the broken path.
robot.straight(100)
robot.turn(90)
while True:
    if lf.isOnPath():
        robot.stop()
        robot.straight(70)
        robot.turn(-90)
        break
    else:
        robot.drive(100, 0)

# Begin LineFollower again, once it finds the new path.
lf.run()

# 2. wall - solution for the 2. broken path.
robot.straight(100)
robot.turn(-90)
while True:
    if lf.isOnPath():
        robot.stop()
        robot.straight(70)
        robot.turn(90)
        break
    else:
        robot.drive(100, 0)

# Begins LineFollower again, once it finds the new line.
lf.run()


# 3. wall - solution for bottle-pickup.
# Contains a right turn and picking up bottle.

# First, the robot has to make a left turn. The more precise we can make it,
# the better, as we want the robot to face the bottle directly, when having
# performed the turn. This is due to the touch sensor.

# I have chosen to make a 45 degree turn, then have the robot drive 2 cm.
robot.turn(60)
robot.straight(80)

# ------- | start TODO 1 | -------
# TODO: Assistiance from distance sensor and a simplification of infinite loops

# Then is will drive until it finds the path.
while True:
    if lf.isOffPath():
        robot.drive(50, 0)
    if lf.isOnPath():
        # When it finds the path, it will drive 2,5 cm divided by
        # cos(45 degrees) = 3,5 cm. This way, it should be in
        # the middle of the path.
        robot.straight(60)
        break

while True:
    if lf.isOffPath():
        robot.turn(3)
    if lf.isOnPath():
        robot.turn(66)
        # It will now open the claw.
        claw_motor.run_time(-1000, 2300)
        break


# Now it will drive, until it meets the bottle.
while True:
    robot.drive(100, 0)
    ev3.screen.print(line_sensor.reflection())
    if touch_sensor.pressed():
        robot.stop()
        ev3.screen.print(line_sensor.reflection())
        claw_motor.run_time(1000, 2000, wait=True)
        break
claw_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)

# At this point, the robot has grabbed the bottle.
# Now it will drive until it finds the 4. wall.

while True:
    # if line_sensor.reflection() < 30:
    if not lf.isOffPath():
        robot.drive(100, 0)
    # if line_sensor.reflection() > 30:
    if lf.isOffPath():
        break

while True:
    if not lf.isOnWall():
        robot.drive(100, 0)
    if lf.isOnWall():
        robot.stop()
        break

# ------- | stop TODO 1 | -------

# 4. wall -
# Contains placing the bottle again and returning to the original path.

# When the robot meets the 4. wall, it will let go of the bottle, back up,
# set the claw into driving position, turn 135 degrees to the left.

claw_motor.run_time(-1000, 2000, wait=True)
claw_motor.run_until_stalled(-1000, then=Stop.COAST, duty_limit=30)
robot.straight(-400)
claw_motor.run_time(1000, 2500)
robot.turn(-180)
robot.straight(150)

# The robot will now drive until it finds the path again.

while True:
    if lf.isOffPath():
        robot.drive(100, 0)
    if lf.isOnPath():
        robot.straight(60)
        robot.turn(80)
        break

# Now the robot will begin linefollowing until the next wall.
lf.run()


# 5. wall - left turn onto seesaw path.
robot.straight(80)
lf.run()

# 6. wall - solution for seesaw.
# Contains crossing the seesaw and another left turn.


# 7. wall - solution for parallel paths.
# Contains changing path twice on the left side of the robot.
robot.straight(200)
robot.turn(-65)
robot.straight(-200)

for n in range(6):
    robot.drive(100, 0)
    while True:
        if n % 2 == 0 and lf.isOffPath():
            ev3.screen.print(n)
            break
        elif n % 2 == 1 and lf.isOnPath():
            ev3.screen.print(n)
            break
        else:
            pass  # Does nothing

robot.straight(70)
robot.turn(45)

# ------- | Legacy Code | --------

# n = 0
# while True:
#     if n == 0:
#         robot.drive(100,0)
#         if lf.isOffPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.drive(100,0)

#     if n == 1:
#         robot.drive(100,0)
#         if lf.isOnPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.drive(100,0)

#     if n == 2:
#         robot.drive(100,0)
#         if lf.isOffPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.drive(100,0)

#     if n == 3:
#         robot.drive(100,0)
#         if lf.isOnPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.drive(100,0)

#     if n == 4:
#         if lf.isOffPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.drive(100,0)

#     if n == 5:
#         if lf.isOnPath():
#             n += 1
#             ev3.screen.print(n)
#             robot.straight(70)
#             robot.turn(45)
#             break

# -------- | end Legacy Code | --------

lf.run()


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
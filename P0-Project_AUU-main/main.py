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
cal = Calibration(ev3, robot, line_sensor, lf)
cal.run()
"""
gyro_sensor.reset_angle(0)
ev3.screen.print(gyro_sensor.angle())
wait(100)
ev3.screen.clear()
ev3.screen.print(ultrasonic_sensor.distance())
wait(100)

"""
claw_motor.run_time(1000, 2500, wait=True)

lf.run()

# After first wall, LineFollower loop will break and
# begin on the following solution for the broken path.
robot.straight(100)
robot.turn(55)
while True:
    if lf.isOnPath():
        robot.straight(50)
        robot.turn(-30)
        break
    else:
        robot.drive(100, 0)

while True:
    if lf.isOnPath():
        robot.drive(100, 0)
    elif lf.isOffPath():
        break

"""
while True:
    if lf.isOffPath():
        robot.turn(-5)
    elif lf.isOnPath():
        break
    else:
        robot.drive(100, 0)
"""

# Begin LineFollower again, once it finds the new path.
lf.run()

# 2. wall - solution for the 2. broken path.
robot.straight(100)
robot.turn(-55)
while True:
    if lf.isOnPath():
        robot.straight(30)
        robot.turn(30)
        break
    else:
        robot.drive(100, 0)

while True:
    if lf.isOnPath():
        robot.drive(100, 0)
    elif lf.isOffPath():
        
        break


# Begins LineFollower again, once it finds the new line.
lf.run()
robot.straight(50)


# 3. wall - solution for bottle-pickup.
# Contains a right turn and picking up bottle.

# First, the robot has to make a left turn. The more precise we can make it,
# the better, as we want the robot to face the bottle directly, when having
# performed the turn. This is due to the touch sensor.

# I have chosen to make a 45 degree turn, then have the robot drive 2 cm.
while True:
    if lf.isOnPath():
        robot.drive(50,0)
    if lf.isOffPath():
        robot.stop()
        claw_motor.run_time(-1000, 2000, wait=True)
        break
claw_motor.run_until_stalled(-1000, then=Stop.HOLD, duty_limit=30)


while True:
    if lf.isOffPath():
        robot.drive(50,0)
    if lf.isOnPath():
        break

robot.straight(130)
while True:
    if ultrasonic_sensor.distance() > 700:
        robot.turn(-2)
    elif 700 >= ultrasonic_sensor() >= 30:
        robot.drive(25,0)
    else:
        robot.stop()
        ev3.speaker.beep(100, 1)
        break
"""
while True:
    if lf.isOffPath():
        robot.drive(-50,0)
    if lf.isOnPath():
        robot.stop()
        break


while True:
    if ultrasonic_sensor.distance() > 1000:
        
    elif 1000 > ultrasonic_sensor() >= 30:
        robot.drive(25,0)
    elif ultrasonic_sensor() <= 30:
        robot.stop()
        break
"""
claw_motor.run_time(1000, 2000, wait=True)
claw_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)


# ------- | start TODO 1 | -------
# TODO: Assistiance from distance sensor and a simplification of infinite loops

# Then is will drive until it finds the path.
    

# Now it will drive, until it meets the bottle.


# At this point, the robot has grabbed the bottle.
# Now it will drive until it finds the 4. wall.

while True:
    # if line_sensor.reflection() < 30:
    if not lf.isOnWall():
        robot.drive(-100, 0)
    # if line_sensor.reflection() > 30:
    if lf.isOnWall():
        break


# ------- | stop TODO 1 | -------

# 4. wall -
# Contains placing the bottle again and returning to the original path.

# When the robot meets the 4. wall, it will let go of the bottle, back up,
# set the claw into driving position, turn 135 degrees to the left.

claw_motor.run_time(-1000, 2000, wait=True)
claw_motor.run_until_stalled(-1000, then=Stop.COAST, duty_limit=30)
robot.reset()
while robot.distance() < 400:
    lf.run()

claw_motor.run_time(1000, 2500)


# Now the robot will begin linefollowing until the next wall.
lf.run()

# 5. wall - left turn onto seesaw path.
robot.turn(-55)
robot.straight(50)
while True:
    if lf.isOnPath():
        robot.straight(30)
        break
    else:
        robot.drive(100, 0)

while True:
    if lf.isOnPath():
        robot.drive(100, 0)
    elif lf.isOffPath():
        break

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
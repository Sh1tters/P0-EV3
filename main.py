#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Stop
from pybricks.robotics import DriveBase

from helper_classes import LineFollower, Calibration

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.D, Direction.CLOCKWISE)
right_motor = Motor(Port.A, Direction.CLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)
claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
line_sensor_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
ultrasonic_sensor = UltrasonicSensor(Port.S1)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=68.8, axle_track=120)

# Make Line Follower
lf = LineFollower(ev3, robot, line_sensor)

# Make Calibration
cal = Calibration(ev3, robot, line_sensor, lf)
line_sensor_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)
line_sensor_motor.run_time(-500, 800, wait=True)
cal.run()
lf.run(250)

# After first wall, LineFollower loop will break and
# begin on the following solution for the broken path.
robot.straight(100)
robot.turn(-65)

while True:
    if lf.isOnPath():
        robot.straight(40)
        robot.turn(55)
        break
    else:
        robot.drive(100, 0)


# Begin LineFollower again, once it finds the new path.
lf.run(200)

# 2. wall - solution for the 2. broken path.
robot.straight(100)
robot.turn(55)
while True:
    if lf.isOnPath():
        robot.straight(100)
        robot.turn(-55)
        break
    else:
        robot.drive(100, 0)

# Begins LineFollower again, once it finds the new line.
lf.run(300)


# 3. wall - solution for bottle-pickup.
# Contains a right turn and picking up bottle.

# First, the robot has to make a left turn. The more precise we can make it,
# the better, as we want the robot to face the bottle directly, when having
# performed the turn. This is due to the touch sensor.

# I have chosen to make a 45 degree turn, then have the robot drive 2 cm
robot.turn(-60)
robot.straight(20)

robot.drive(80, 0)
while True:
    if lf.isOnPath():
        break

while True:
    if lf.isOffPath():
        robot.stop()
        break

robot.straight(80)
while True:
    if 121 < ultrasonic_sensor.distance() < 400:
        robot.drive(50, 0)
    elif ultrasonic_sensor.distance() <= 120:
        robot.stop()
        break
    else:
        robot.drive(0, -25) #40

robot.straight(88)
claw_motor.run_time(1000, 1000, wait=True)
claw_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)
robot.straight(230)
claw_motor.run_time(-1000, 1800, wait=True)
robot.straight(-200)
robot.turn(130)
robot.straight(100)
robot.drive(400, 0)
while True:
    if lf.isOnPath():
        robot.straight(70)
        robot.turn(-15)
        robot.stop()
        break

lf.run(250)

# 5. wall and 6. wall: Seesaw line up and seesaw
robot.straight(180)
robot.turn(90)
lf.run(50)
line_sensor_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)
robot.straight(600)
robot.stop()
robot.settings(50,640,153,611)
robot.straight(500)
robot.stop()
robot.settings(160,640,153,611)
robot.straight(850)
line_sensor_motor.run_time(-500, 800, wait=True)
robot.turn(75)
robot.straight(50)
while True:
    if lf.isOnPath():
        break
    else:
        robot.drive(100, 0)
lf.run(100)

# 7. wall - solution for parallel paths.
# Contains changing path twice on the left side of the robot.
robot.straight(200)
robot.turn(65)
robot.straight(-120)

for n in range(6):
    robot.drive(100, 0)
    while True:
        if n % 2 == 0 and lf.isOffPath():
            break
        elif n % 2 == 1 and lf.isOnPath():
            break
        else:
            pass  # Does nothing

robot.straight(70)
robot.turn(-55)
lf.run(250)

# 8. wall bullseye lineup
robot.turn(60)
robot.straight(20)
robot.drive(200, 0)
while True:
    if lf.isOnPath():
        robot.turn(10)
        robot.stop()
        break
robot.straight(20)
robot.turn(35)
lf.run(50)

# 9. wall bullseye
robot.straight(100)

for n in range(6):
    robot.drive(100, 0)
    while True:
        if n % 2 == 0 and lf.isOffPath():
            break
        elif n % 2 == 1 and lf.isOnPath():
            break
        else:
            pass  # Does nothing

robot.stop()
robot.straight(50)
robot.turn(32)
robot.straight(470)
claw_motor.run_time(1000, 1000, wait=True)
claw_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=40)
robot.straight(-580)
robot.straight(55)
claw_motor.run_time(-1000, 1800, wait=True)
robot.straight(-470)
robot.turn(-40)
robot.drive(-100, 0)
claw_motor.run_time(1000, 2000, wait=True)
while not lf.isOnPath(): pass
robot.stop()
robot.turn(-80)
lf.run(200)

# 10. wall around bottle
robot.turn(-40)
robot.straight(400)
robot.turn(50)
robot.straight(330)
lf.run(175)

# 11. wall maze/tunnel
while True:
    if ultrasonic_sensor.distance() > 120:
        robot.drive(100, 0)
    else: break
robot.stop()
robot.turn(80)
robot.straight(120)
robot.turn(-50)
robot.straight(210)
robot.turn(-60)
robot.straight(280)
robot.turn(30)
robot.straight(310)
lf.run(100)

# 12. wall around bottle
robot.turn(-30)
robot.straight(400)
robot.turn(65)
while True:
    if lf.isOffPath():
        robot.drive(200, 0)
    else: break

robot.stop()
robot.turn(-20)
lf.run(200)

# 13. wall runway
robot.turn(11)
robot.straight(1650)

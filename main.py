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
line_sensor_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30) # Lift the sensor up
line_sensor_motor.run_time(-500, 800, wait=True) # Lifts the sensor down
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
robot.turn(-65)
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
    if 121 < ultrasonic_sensor.distance() < 400: # Drives to the bottle until its distance is less than 12 cm
        robot.drive(50, 0)
    elif ultrasonic_sensor.distance() <= 120: # The robot has reached the bottle at a distance of 12 cm
        robot.stop()
        break
    else:
        robot.drive(0, -25) # The robot will spin until it finds the bottle

robot.straight(88)
claw_motor.run_time(1000, 1000, wait=True) # Close slightly the claw
claw_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30) # Closes the remaining until it has stalled
robot.straight(230)
robot.straight(-20)
claw_motor.run_time(-1000, 1800, wait=True) # Open the claw
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
robot.stop()
robot.settings(200,640,153,611)
robot.straight(450)

robot.stop()
robot.settings(50,640,153,611)
line_sensor_motor.run_time(-500, 800, wait=True)
robot.straight(700)
line_sensor_motor.run_until_stalled(1000, then=Stop.HOLD, duty_limit=30)

robot.stop()
robot.settings(160,640,153,611)
robot.straight(600)
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
    """
    Everytime a statement is true, then we break out of the current
    loop index position, and into a new index position. At last it will
    have hit the third path and be out of the for loop.
    """
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
    """
    Everytime a statement is true, then we break out of the current
    loop index position, and into a new index position. At last it will
    have hit the third path and be out of the for loop.
    """
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
robot.turn(31)
robot.straight(460)
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
    if ultrasonic_sensor.distance() > 130:
        robot.drive(100, 0)
    else: break
robot.stop()
robot.turn(45)
while True:
    if ultrasonic_sensor.distance() > 120:
        robot.drive(100, 0)
    else: break
robot.turn(-85)
robot.straight(270)
robot.turn(40)
robot.straight(280)
lf.run(100)

# 12. wall around bottle
robot.turn(-30)
robot.straight(450)
robot.turn(65)
while True:
    if lf.isOffPath():
        robot.drive(200, 0)
    else: break

robot.straight(30)
robot.stop()
robot.turn(-20)
lf.run(200)

# 13. wall runway
robot.turn(11)
robot.straight(1650)
claw_motor.run_time(-1000, 1800, wait=True)


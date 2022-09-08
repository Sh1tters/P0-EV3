from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json

class LineFollower:
    def __init__(self, robot: DriveBase, line_sensor: ColorSensor, ev3: EV3Brick, path_value: int, wall_value: int, accepted_deviance, turn_angle: int, drive_speed: int):
        self.robot = robot
        self.line_sensor = line_sensor
        self.ev3 = ev3
        self.path_value = path_value
        self.wall_value = wall_value
        self.accepted_deviance = accepted_deviance
        self.turn_angle = turn_angle
        self.drive_speed = drive_speed
        self.shut_down = False
    
    def isOnPath(self) -> bool:
        return self.path_value + self.accepted_deviance > self.line_sensor.reflection() > self.path_value - self.accepted_deviance

    def isOnWall(self) -> bool:
        return self.wall_value + self.accepted_deviance > self.line_sensor.reflection() > self.wall_value - self.accepted_deviance

    def isOffPath(self) -> bool:
        return not self.isOnPath() and not self.isOnWall()

    def autocorrectPath(self) -> None:
        self.robot.stop()

        swing_multiplier = 1
        direction = 1
        while self.isOffPath() and swing_multiplier * self.turn_angle < 90:
            #ba = 1
            #if d < 0:
            #    ba = 2
            
            self.robot.turn(self.turn_angle * swing_multiplier * direction)

            if self.isOnPath():
                break

            self.robot.turn(self.turn_angle * swing_multiplier * -direction)

            if direction < 0:
                swing_multiplier += 1
            
            direction *= -1

    def adjust_lane(self) -> None:
        pass

    def run(self) -> None:
        # Run Loop
        while not self.shut_down:
            #self.ev3.screen.print(self.path_value, self.line_sensor.reflection())
            if self.isOnWall():
                self.robot.stop()
                # TODO: Change to challenge modes
            elif self.isOffPath():
                self.autocorrectPath()
            else:
                self.robot.drive(self.drive_speed, 0)
                wait(10)

class Calibration:

    def __init__(self, robot: DriveBase, ev3: EV3Brick, line_sensor: ColorSensor) -> None:
        self.robot = robot
        self.ev3 = ev3
        self.line_sensor = line_sensor
        self.calibrated = False

    def run(self) -> None:
        while not self.calibrated:
            self.ev3.screen.print('Calibrating...')

            # First sample measurement
            pv_s1 = self.line_sensor.reflection()

            # Move sensor to unique position
            self.robot.straight(100)
            wait(100)

            # Second sample measurement
            pv_s2 = self.line_sensor.reflection()

            # Move sensor to unique position
            self.robot.straight(-80)
            wait(100)

            # Third sample measurement
            pv_s3 = self.line_sensor.reflection()

            self.path_value = int((pv_s1 + pv_s2 + pv_s3) / 3)
            self.ev3.screen.clear()
            self.ev3.screen.print('PATH_VALUE: %s' % path_value)

            # change settings.py path values
            data = {"PATH_VALUE": self.path_value}

            with open('config.json', 'w') as jsonfile:
                json.dump(data, jsonfile)
            self.calibrated = True

            #Calibration DONE
            self.ev3.screen.clear()
            self.ev3.screen.print('Calibration done')
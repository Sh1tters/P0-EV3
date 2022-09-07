from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json

class LineFollower:
    def __init__(self, robot: DriveBase, line_sensor: ColorSensor, path_value: int, wall_value: int, accepted_deviance, turn_angle: int, drive_speed: int):
        self.robot = robot
        self.line_sensor = line_sensor
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
            if self.isOnWall():
                self.robot.stop()
                # TODO: Change to challenge modes
            elif self.isOffPath():
                self.autocorrectPath()
            else:
                self.robot.drive(self.drive_speed, 0)
                wait(10)

class Calibration:
    def __init__(self, robot: DriveBase, ev3: EV3Brick, line_sensor: ColorSensor, lf: LineFollower) -> None:
        self.robot = robot
        self.ev3 = ev3
        self.line_sensor = line_sensor
        self.lf = lf
        self.calibrated = False

    def run(self) -> None:
        while not self.calibrated:
            self.ev3.screen.print('Calibrating...')
            pv1 = self.line_sensor.reflection()
            wait(200)
            
            self.robot.straight(50)
            pv2 = self.line_sensor.reflection()
            wait(200)

            self.robot.straight(-40)
            pv3 = self.line_sensor.reflection()
            wait(200)

            path_value = int((pv1 + pv2 + pv3) / 3)
            wait(800)
            self.ev3.screen.clear()
            self.ev3.screen.print(f'Found path value {path_value}')
            wait (500)

            # change settings.py path values
            jsonDump = json.dumps({"PATH_VALUE", path_value})
            jsonFile = open("config.json", "w")
            jsonFile.write(jsonDump)
            jsonFile.close()
            self.calibrated = True

            #Calibration DONE
            self.ev3.screen.clear()
            self.ev3.screen.print(f'Calibration done')

            # Run linefollower
            self.lf.run()


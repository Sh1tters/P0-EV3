import time
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json

class LineFollower:  
    def __init__(self, ev3: EV3Brick, robot: DriveBase, line_sensor: ColorSensor):
        """__init__ Constructs the necessary variables and objects to build a line follower

        Args:
            ev3 (EV3Brick): The mindstorms brick
            robot (DriveBase): The robot DriveBase
            line_sensor (ColorSensor): The sensor to detect the line
        """        
        self.robot = robot
        self.ev3 = ev3
        self.line_sensor = line_sensor
        self.path_value = 0
    
    def isOnPath(self) -> bool:
        """isOnPath Check if robot is on path

        Returns:
            bool: Is on path
        """        
        return self.line_sensor.reflection() <= self.path_value

    def isOnWall(self) -> bool:
        """isOnWall Check if robot is on a wall

        Returns:
            bool: Is on wall
        """        
        return 20 > self.line_sensor.reflection()

    def isOffPath(self) -> bool:
        """isOffPath Check if robot is off path

        Returns:
            bool: Is off path
        """        
        return not self.isOnPath() and not self.isOnWall()


    def FollowPath(self, DRIVE_SPEED) -> None:
        """autocorrectPath Autocorrect to the path
        """        
        while not self.isOnWall():
            # Calculate the deviation
            deviation = self.path_value - self.line_sensor.reflection()
            proportional_gain = 2

            # Calculate the turn rate
            turn_rate = proportional_gain * deviation * (DRIVE_SPEED/250)

            self.robot.drive(DRIVE_SPEED, int(turn_rate))


    def run(self, DRIVE_SPEED) -> None:
        """run Run the Line Following
                """
        # Run Loop
        while True:
            if self.isOnWall() :
                self.robot.stop()
                break
            else:
                self.FollowPath(DRIVE_SPEED)

class Calibration:
    def __init__(self, ev3: EV3Brick, robot: DriveBase, line_sensor: ColorSensor, lf: LineFollower) -> None:
        self.robot = robot
        self.line_sensor = line_sensor
        self.calibrated = False
        self.lf = lf
        self.ev3 = ev3

    def run(self) -> None:
        while not self.calibrated:
            self.robot.turn(-15)

            # First sample measurement
            pv_s1 = self.line_sensor.reflection()
            self.ev3.screen.print(self.line_sensor.reflection())
            wait(50)

            # Move sensor to unique position
            self.robot.turn(30)

            # Second sample measurement
            pv_s2 = self.line_sensor.reflection()
            self.ev3.screen.print(self.line_sensor.reflection())
            wait(50)

            # Move sensor to first position
            self.robot.turn(-15)
            self.ev3.screen.print(self.line_sensor.reflection())

            # Calculate average value between samples
            path_value = int((pv_s1 + pv_s2) / 2)
            wait(50)

            # change config.json path values
            data = {"PATH_VALUE": path_value}

            with open('config.json', 'w') as jsonfile:
                json.dump(data, jsonfile)
            self.calibrated = True

            # Run Linefollower
            self.lf.path_value = path_value

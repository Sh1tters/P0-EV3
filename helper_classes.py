from time import time
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json, time

class LineFollower:  
    def __init__(self, robot: DriveBase, line_sensor: ColorSensor, path_value: int, wall_value: int, accepted_deviance: int, turn_angle: int, drive_speed: int):
        """__init__ Constructs the necessary variables and objects to build a line follower

        Args:
            robot (DriveBase): The robot DriveBase
            line_sensor (ColorSensor): The sensor to detect the line
            path_value (int): Reflection value of the line
            wall_value (int): Reflection valie of the walls
            accepted_deviance (int): The accepted deviance/change in reflection
            turn_angle (int): The angle of which we want to turn
            drive_speed (int): The speed we want to drive
        """        
        self.robot = robot
        self.line_sensor = line_sensor
        self.path_value = path_value
        self.wall_value = wall_value
        self.accepted_deviance = accepted_deviance
        self.turn_angle = turn_angle
        self.drive_speed = drive_speed
        self.shut_down = False
        self.last_turn_direction = 1
        self.last_autocorrect_time = 0
        self.autocorrect_timeframe = 1
        self.comulative_turn_size = 10
        self.comulative_turn = 0
        self.last_decay_time = 0
        self.decay_timeframe = 1
    
    def isOnPath(self) -> bool:
        """isOnPath Check if robot is on path

        Returns:
            bool: Is on path
        """        
        return self.path_value + self.accepted_deviance >= self.line_sensor.reflection() >= self.path_value - self.accepted_deviance

    def isOnWall(self) -> bool:
        """isOnWall Check if robot is on a wall

        Returns:
            bool: Is on wall
        """        
        return self.path_value - self.accepted_deviance > self.line_sensor.reflection()

    def isOffPath(self) -> bool:
        """isOffPath Check if robot is off path

        Returns:
            bool: Is off path
        """        
        return not self.isOnPath() and not self.isOnWall()

    def autocorrectPath(self) -> None:
        """autocorrectPath Autocorrect to the path
        """        
        self.robot.stop()

        swing_multiplier = 1
        direction = self.last_turn_direction
        while self.isOffPath() and swing_multiplier * self.turn_angle < 90:
            
            self.robot.turn(self.turn_angle * swing_multiplier * direction)

            if self.isOnPath():
                break

            self.robot.turn(self.turn_angle * swing_multiplier * -direction)

            if direction != self.last_turn_direction:
                swing_multiplier += 1
            
            direction *= -1
        
        if not swing_multiplier * self.turn_angle < 90:
            self.robot.straight(10)
        
        if self.last_autocorrect_time >= int(time.time()) - self.autocorrect_timeframe:
            self.comulative_turn += direction * self.comulative_turn_size
        
        self.last_autocorrect_time = self.last_decay_time = int(time.time())
        self.last_turn_direction = direction

    def run(self) -> None:
        """run Run the Line Following
        """        
        # Set autocorrect time
        self.last_autocorrect_time = self.last_decay_time = int(time.time())

        # Run Loop
        while not self.shut_down:
            if self.isOnWall():
                self.robot.stop()
                self.comulative_turn = 0
                self.last_turn_direction = 1
                break
                # TODO: Change to challenge modes
            elif self.isOffPath():
                self.autocorrectPath()
            else:
                self.robot.drive(self.drive_speed, self.comulative_turn)
                if self.last_decay_time + self.decay_timeframe <= int(time.time()) and self.comulative_turn != 0:
                    self.comulative_turn -= (self.comulative_turn/(self.comulative_turn**2)**.5) * self.comulative_turn_size
                    self.last_decay_time = int(time.time())

class Calibration:
    def __init__(self, robot: DriveBase, line_sensor: ColorSensor, lf: LineFollower) -> None:
        self.robot = robot
        self.line_sensor = line_sensor
        self.calibrated = False
        self.lf = lf

    def run(self) -> None:
        while not self.calibrated:

            # First sample measurement
            pv_s1 = self.line_sensor.reflection()

            # Move sensor to unique position
            self.robot.straight(50)

            # Second sample measurement
            pv_s2 = self.line_sensor.reflection()

            # Move sensor to unique position
            self.robot.straight(-30)

            # Third sample measurement
            pv_s3 = self.line_sensor.reflection()

            path_value = int((pv_s1 + pv_s2 + pv_s3) / 3)

            # change settings.py path values
            data = {"PATH_VALUE": path_value}

            with open('config.json', 'w') as jsonfile:
                json.dump(data, jsonfile)
            self.calibrated = True

            # Run Linefollower
            self.lf.path_value = path_value
from time import time
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json

from settings import DRIVE_SPEED, GREY_VALUE, PATH_VALUE

class LineFollower:  
    def __init__(self, ev3: EV3Brick, robot: DriveBase, line_sensor: ColorSensor, path_value: int, wall_value: int, accepted_deviance: int, turn_angle: int, drive_speed: int):
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
        self.ev3 = ev3
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
        self.decay_timeframe = .5
    
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
        return 20 > self.line_sensor.reflection()

    def isOffPathGrey(self) -> bool:
        return self.line_sensor.reflection() < self.path_value

    def isOffPath(self) -> bool:
        """isOffPath Check if robot is off path

        Returns:
            bool: Is off path
        """        
        return not self.isOnPath() and not self.isOnWall()


    def FollowPath(self) -> None:
        """autocorrectPath Autocorrect to the path
        """        
        while not self.isOnWall():
            deviation = self.path_value - self.line_sensor.reflection()
            proportional_gain = 1.6
            turn_rate = proportional_gain * deviation

        
       
            self.ev3.screen.print("FollowPath")
            self.robot.drive(DRIVE_SPEED, int(turn_rate))
            wait(1)
    
    def ReverseFollowPath(self) -> None:
        """autocorrectPath Autocorrect to the path
        """        
        while not self.isOnWall():
            deviation = self.path_value - self.line_sensor.reflection()
            proportional_gain = 1.6
            turn_rate = proportional_gain * deviation

        
       
            self.ev3.screen.print("FollowPath")
            self.robot.drive(-DRIVE_SPEED, int(turn_rate))
            wait(1)




    def run(self) -> None:
        """run Run the Line Following
                """

        # Run Loop
        while True:
            if self.isOnWall():
                self.robot.stop()
                self.ev3.screen.print("Black Wall")
                wait(10)
                break
                # TODO: Change to challenge modes
            else:
                self.FollowPath()
                self.ev3.screen.print(self.path_value - self.line_sensor.reflection())


    def reverse_run(self) -> None:
        """run Run the Line Following
                """
         # Run Loop
        while True:
            if self.isOnWall():
                self.robot.stop()
                self.ev3.screen.print("Black Wall")
                wait(10)
                break
                # TODO: Change to challenge modes
            else:
                self.ReverseFollowPath()
                self.ev3.screen.print(self.path_value - self.line_sensor.reflection())
                
        
            
                

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
            wait(500)
            

            # Move sensor to unique position
            self.robot.turn(30)

            # Second sample measurement
            pv_s2 = self.line_sensor.reflection()
            self.ev3.screen.print(self.line_sensor.reflection())
            wait(500)

            # Move sensor to unique position
            self.robot.turn(-15)
            self.ev3.screen.print(self.line_sensor.reflection())
            wait(1000)

            # Third sample measurement
            #pv_s3 = self.line_sensor.reflection()

            path_value = int((pv_s1 + pv_s2) / 2)

        

            # change settings.py path values
            data = {"PATH_VALUE": path_value, "GREY_VALUE": pv_s1}

            with open('config.json', 'w') as jsonfile:
                json.dump(data, jsonfile)
            self.calibrated = True

            # Run Linefollower
            self.lf.path_value = path_value

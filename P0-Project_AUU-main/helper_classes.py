import time
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
import json

class LineFollower:  
    def __init__(self, ev3: EV3Brick, robot: DriveBase, line_sensor: ColorSensor, path_value: int, wall_value: int, accepted_deviance: int, turn_angle: int):
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
            deviation = self.path_value - self.line_sensor.reflection()
            proportional_gain = 2
            turn_rate = proportional_gain * deviation * (DRIVE_SPEED/250)

            self.robot.drive(DRIVE_SPEED, int(turn_rate))


    def run(self, DRIVE_SPEED, drive_time=None) -> None:
        """run Run the Line Following
                """
        start_time = time.time()
        debug_big_nums = (int(start_time) // 100) * 100
        # Run Loop
        while True:
            self.ev3.screen.print(str(int(start_time)-debug_big_nums) + " " + str(int(time.time())-debug_big_nums) + " " + str(drive_time))     
            if self.isOnWall() or (drive_time != None and time.time() - start_time >= drive_time):
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
            data = {"PATH_VALUE": path_value, "GREY_VALUE": pv_s1}

            with open('config.json', 'w') as jsonfile:
                json.dump(data, jsonfile)
            self.calibrated = True

            # Run Linefollower
            self.lf.path_value = path_value

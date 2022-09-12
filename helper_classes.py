from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait
from os import listdir
import json

class LineFollower:  
    def __init__(self, robot: DriveBase, line_sensor: ColorSensor, path_value: int, accepted_deviance: int, turn_angle: int, drive_speed: int):
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
        self.accepted_deviance = accepted_deviance
        self.turn_angle = turn_angle
        self.drive_speed = drive_speed
        self.shut_down = False
    
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
        direction = 1
        while self.isOffPath() and swing_multiplier * self.turn_angle < 90:
            
            self.robot.turn(self.turn_angle * swing_multiplier * direction)

            if self.isOnPath():
                break

            self.robot.turn(self.turn_angle * swing_multiplier * -direction)

            if direction < 0:
                swing_multiplier += 1
            
            direction *= -1
    
    def calibrate(self, sample_size: int = 3) -> int:
        """calibrate Calibrate the reflection value of the track

        Args:
            sample_size (int, optional): The amount of samples there should be taken. Defaults to 3.

        Returns:
            int: The average reflection value of the track
        """        
        samples = list()
        for i in range(sample_size):
            samples.append(self.line_sensor.reflection())
            self.robot.straight(50)
            wait(100)
        
        self.path_value = sum(samples)/sample_size
        return self.path_value

    def run(self) -> None:
        """run Run the Line Following
        """        
        # Run Loop
        while not self.shut_down:
            if self.isOnWall():
                self.robot.stop()
                break
                # TODO: Change to challenge modes
            elif self.isOffPath():
                self.autocorrectPath()
            else:
                self.robot.drive(self.drive_speed, 0)

class SettingsManager():
    def __init__(self) -> None:
        """__init__ Constructs the SettingsManager
        """        
        self._settings = dict()
    
    def checkSettingsFileExists(self) -> bool:
        """checkSettingsFileExists Checks if 'config.json' exists

        Returns:
            bool: File exists
        """        
        return 'config.json' in listdir()
    
    def checkSettingsExist(self) -> bool:
        """checkSettingsExist Checks of the internal settings dictionary exists

        Returns:
            bool: Dictionary exists
        """                
        return len(self._settings) > 0
    
    def checkIfSettingKeyExists(self, key: str) -> bool:
        """checkIfSettingKeyExists Checks if the settings key exists in the internal settings dictionary

        Args:
            key (str): Key to check

        Returns:
            bool: Key exists
        """        
        return key in self._settings.keys()

    def loadSettings(self) -> bool:
        """loadSettings Loads settings from 'config.json' into the internal settings dictionary

        Returns:
            bool: Settings loaded
        """           
        if self.checkSettingsFileExists():
            with open("config.json", "r") as fp:
                self._settings = json.load(fp)
            return True
        return False

    def setSetting(self, key: str, value) -> bool:
        """set_setting Set/change setting in the internal settings dictionary

        Args:
            key (str): Key to set to
            value (Any): Value to set

        Returns:
            bool: Setting is set
        """        
        if self.checkSettingsFileExists() and self.checkSettingsExist():
            self._settings[key] = value
            return True
        return False

    def getSetting(self, key: str):
        """get_setting Get a setting value

        Args:
            key (str): Key to get from

        Returns:
            Any: Value from key or None if key didn't exist
        """        
        if self.checkIfSettingKeyExists:
            return self._settings[key]
        return None
from pybricks.robotics import DriveBase
from pybricks.ev3devices import ColorSensor
from pybricks.tools import wait

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
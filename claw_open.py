#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction

claw_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)


claw_motor.run_time(-1000,1800)
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

ev3 = EV3Brick()

"""
ev3.speaker.play_notes([], tempo=180)
16'th note break: wait(83)
8'th note break: wait(167)
4'th note break: wait(333)
1/2'th note break: wait(666)
whole note break: wait(1333)

"""

def p16(): wait(83)
def p8(): wait(167)
def p4(): wait(33)
def p2(): wait(666)
def p1(): wait(1333)


ev3.speaker.play_notes(["E4/8","E4/8."], tempo=180)
p8()
ev3.speaker.play_notes(["E4/8"], tempo=180)
p8()
ev3.speaker.play_notes(["C4/8","E4/4","G4/4"], tempo=180)
p4()
p8()
ev3.speaker.play_notes(["G3/4"], tempo=180)
p4()
p8()

for _ in range(2):
    ev3.speaker.play_notes(["C4/4"], tempo=180)
    p8()
    ev3.speaker.play_notes(["G3/4"], tempo=180)
    p8()
    ev3.speaker.play_notes(["E3/4"], tempo=180)
    p8()
    ev3.speaker.play_notes(["A3/4","B3/4", "Bb3/8","A3/4","G3/8.","E4/8.","G4/8","A4/4","F4/8","G4/8"], tempo=180)
    p8()
    ev3.speaker.play_notes(["E4/4","C4/8","D4/8","B3/4"], tempo=180)
    p8()

    
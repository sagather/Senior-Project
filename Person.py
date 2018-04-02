# Simple class to create a Person object

class Person():
    personCount = 0
    color = [0, 0, 0]
    # _motionStateArray = [topleft, topright, bottomleft, bottomright, bothtop, bothbottom]
    motion = [0, 0, 0, 0, 0, 0]

    def __init__(self):
        Person.personCount += 1

    def setColor(self, r, g, b):
        self.color = [r, g, b]

    def setMotion(self, index, value):
        self.motion[index] = value

    def clearMotion(self):
        self.motion = [0, 0, 0, 0, 0, 0]
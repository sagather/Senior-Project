# Simple class to create a Person object

class Person():
    personCount = 0
    color = [0, 0, 0]
    # _motionStateArray = [topleft, topright, bottomleft, bottomright]
    motion = [0, 0, 0, 0]

    def __init__(self):
        Person.personCount += 1

    def setColor(self, r, g, b):
        self.color = [r, g, b]

    def setMotion(self, left, right, lowerl, lowerr):
        self.motion = [left, right, lowerl, lowerr]

    #def setMotion(self, index):
    #    self.motion[index] = 1

    def clearMotion(self):
        self.motion[0] = 0
        self.motion[1] = 0
        self.motion[2] = 0
        self.motion[3] = 0

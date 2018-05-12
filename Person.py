# Simple class to create a Person object

class Person():
    personCount = 0
    color = [0, 0, 0]
    # _motionStateArray = [topleft, topright, bottomleft, bottomright]
    motion = [0, 0, 0, 0]

    def __init__(self):
        Person.personCount += 1

    def setColor(self, r, g, b):    # Takes RGB values and sets those as the color for the person's face
        self.color = [r, g, b]

    def setMotion(self, left, right, lowerl, lowerr):   # Applies passed values to the motion state array
        self.motion = [left, right, lowerl, lowerr]

    #def setMotion(self, index):
    #    self.motion[index] = 1

    def clearMotion(self):  # Resets each position in the motion state array to 0
        self.motion[0] = 0
        self.motion[1] = 0
        self.motion[2] = 0
        self.motion[3] = 0

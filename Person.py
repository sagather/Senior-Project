# Simple class to create a Person object

class Person():
    personCount = 0
    color = [0, 0, 0]

    def __init__(self):
        Person.personCount += 1

    def setColor(self, r, g, b):
        self.color = [r, g, b]
# Simple class to create a Person object

class Person():
    personCount = 0

    def __init__(self, personid):
        Person.personCount += 1
        self.personid = personid
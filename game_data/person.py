"""
Contains the Person class representing characters as game units.
"""

class Person:
    id_count=0
    def __init__(self, max_health):
       self.id=Person.id_count
       self.max_health=self.health=max_health
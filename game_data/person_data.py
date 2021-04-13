"""
Contains the Person class representing characters as game units.
"""

class Person_Data:
    id_count=0
    def __init__(self, max_health):
       self.id=Person_Data.id_count
       Person_Data.id_count +=1
       self.max_health=self.health=max_health
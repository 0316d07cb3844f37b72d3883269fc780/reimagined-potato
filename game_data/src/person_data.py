"""
Contains the Person class representing characters as game units. Contains attributes that persist between fights.
"""

from game_data.src.getter_scene import getter

class Person_Data:
    legal_types = ["Testtype"]
    def __init__(self, max_health, type, deck=[]):
       self.max_health=self.health=max_health

       self.deck=deck

       getter.register(self)

       if(type in Person_Data.legal_types):
           self.type=type
       else:
           raise Exception("Illegal type")

    def damage(self, damage):
        self.health-=damage
        if(self.health <= 0):
            self.die()



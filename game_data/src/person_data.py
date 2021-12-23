"""
Contains the Person class representing characters as game units. Contains attributes that persist between fights.
"""

class Person_Data:
    id_count=0
    legal_types = ["Testtype"]
    def __init__(self, max_health, type):
       self.id=Person_Data.id_count
       Person_Data.id_count +=1
       self.max_health=self.health=max_health
       self.actions=[]
       if(type in Person_Data.legal_types):
           self.type=type
       else:
           raise Exception("Illegal type")

    def damage(self, damage):
        self.health-=damage
        if(self.health <= 0):
            self.die()



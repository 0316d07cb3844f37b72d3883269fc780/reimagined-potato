"""
A person as it is in the Fight_Scene.
"""

from game_data.src.drawpile import Drawpile

class Person_Fighting():
    def __init__(self, base_person):
        self.person=base_person
        self.actions=[]
        self.drawpile=Drawpile(base_person.deck)
        self.resist=0

    def damage(self, damage):
        self.person.damage(damage)

    def get_health(self):
        return self.person.health

    def append_action(self,action):
        self.actions.append(action)

    def die(self):
        pass
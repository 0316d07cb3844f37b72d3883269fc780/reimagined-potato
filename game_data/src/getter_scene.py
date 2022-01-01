"""
Gets all objects of a Scene by ID if possible.
"""

from random import randint
from sys import maxsize

class Getter_Scene():

    def __init__(self):
        self.all_objects={}

    def register(self,object):
        scene_id=randint(0,maxsize)
        self.all_objects[scene_id]=object
        object.scene_id=scene_id
        return scene_id

    def __getitem__(self, scene_id):
        return self.all_objects[scene_id]

getter=Getter_Scene()
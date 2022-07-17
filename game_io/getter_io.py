"""
Gets all objects of the UI by ID if possible.
"""


class GetterIO:
    last_id = 0

    def __init__(self):
        self.all_objects = {}

    def register(self, object):
        scene_id = GetterIO.last_id
        GetterIO.last_id += 1
        self.all_objects[scene_id] = object
        object.scene_id = scene_id
        return scene_id

    def __setitem__(self, new_id, object):
        del (self.all_objects[object.scene_id])
        object.scene_id = new_id
        self.all_objects[new_id] = object

    def __getitem__(self, scene_id):
        return self.all_objects[scene_id]


getter = GetterIO()

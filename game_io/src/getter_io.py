"""
Gets all objects of the UI by ID if possible.
"""


class GetterIO:
    last_id = 0

    def __init__(self):
        self.all_objects = {}

    def register(self, object_to_register):
        scene_id = GetterIO.last_id
        GetterIO.last_id += 1
        self.all_objects[scene_id] = object_to_register
        object_to_register.scene_id = scene_id
        return scene_id

    def __setitem__(self, new_id, object_to_register):
        del (self.all_objects[object_to_register.scene_id])
        object_to_register.scene_id = new_id
        self.all_objects[new_id] = object_to_register

    def __getitem__(self, scene_id):
        return self.all_objects[scene_id]

    def __contains__(self, item):
        return item in self.all_objects


getter = GetterIO()

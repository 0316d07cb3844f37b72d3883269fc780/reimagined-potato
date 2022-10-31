"""
Gets all objects of a Scene by ID if possible.
"""


class GetterScene:
    last_id = 0

    def __init__(self):
        self.all_objects = {}

    def register(self, object_to_register):
        scene_id = GetterScene.last_id
        GetterScene.last_id += 1
        self.all_objects[scene_id] = object_to_register
        object_to_register.scene_id = scene_id
        return scene_id

    def __setitem__(self, new_id, object_to_set):
        del (self.all_objects[object_to_set.scene_id])
        if new_id == "auto":
            self.register(object_to_set)
            return
        object_to_set.scene_id = new_id
        self.all_objects[new_id] = object_to_set

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.all_objects[key]
        else:
            return [self[scene_id] for scene_id in key]


getter = GetterScene()

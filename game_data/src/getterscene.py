"""
Gets all objects of a Scene by ID if possible.
"""


class GetterScene:

    def __init__(self):
        self.all_objects = {}
        self.last_id = 0

    def register(self, object_to_register):
        scene_id = self.last_id
        self.last_id += 1
        self.all_objects[scene_id] = object_to_register
        object_to_register.scene_id = scene_id
        return scene_id

    def __setitem__(self, new_id, object_to_set):
        if object_to_set.scene_id in self.all_objects:
            del (self.all_objects[object_to_set.scene_id])
        if new_id == "auto" or new_id == "":
            self.register(object_to_set)
            return
        object_to_set.scene_id = new_id
        self.all_objects[new_id] = object_to_set
        if not self.last_id > new_id:
            self.last_id = new_id+1

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.all_objects[key]
        else:
            return [self[scene_id] for scene_id in key]


global_getter = GetterScene()


class GetterWrapper:
    def __init__(self, internal_getter):
        self.getter = internal_getter

    def __getitem__(self, item):
        return self.getter[item]

    def register(self, item):
        return self.getter.register(item)

    def __setitem__(self, key, value):
        self.getter[key] = value

    def __contains__(self, key):
        return key in self.getter.all_objects


getter = GetterWrapper(global_getter)


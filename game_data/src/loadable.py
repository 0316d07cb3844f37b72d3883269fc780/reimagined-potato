from utility.src.string_utils import *


class Loadable:
    def save_to_file(self, path: str):
        with open(root_path(path), "w") as file:
            file.write(str(self))

    @classmethod
    def load_from_file(cls, path: str):
        with open(root_path(path), "r") as file:
            file_content = file.read()
        return cls.create_from_string(file_content)

    @classmethod
    def create_from_string(cls, _):
        raise NotImplemented

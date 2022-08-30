import sys
import tkinter
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from enum import Enum
from os import path

from utility.src.string_utils import *


class Mode(Enum):
    card = 0
    person = 1
    team = 1


file_extension_by_mode = {
    Mode.card: ".card",
    Mode.person: ".person",
    Mode.team: ".team"
}

mode_by_file_extension = {}
for mode, extension in file_extension_by_mode.items():
    mode_by_file_extension[extension] = mode

attributes_by_mode = {
    Mode.card: {
        "name": "string",
        "action_factory": "string",
        "speed": "string",
        "target_checker": "string",
        "image": "string"
    },

    Mode.person: {

    },

    Mode.card: {

    }
}

file_types = (("Card File", "*.card"),
              ("Person File", "*.person"))


class Widget:
    widgets = []

    def __init__(self):
        Widget.widgets += self

    def test_entry_legal(self):
        pass

    @classmethod
    def flush(cls):
        widgets = []


class StringAttributeWidget(Widget):
    def __init__(self, master, tag, value):
        self.tag = tag
        attribute_frame = tkinter.Frame(master)
        attribute_label = tkinter.Label(attribute_frame, text=tag)
        self.attribute_value = tkinter.Entry(attribute_frame)
        self.attribute_value.insert(0, value)
        attribute_label.pack(fill=tkinter.X)
        self.attribute_value.pack(fill=tkinter.X)
        attribute_frame.pack(fill=tkinter.X)
        self.attribute_type = "string"

    def value_as_tags(self):
        inner_part = create_tag(self.tag, self.attribute_value.get())
        return create_tag("string", inner_part)

class IntAttributeWidget(Widget):
    def __init__(self, master, tag, value):
        self.tag = tag
        attribute_frame = tkinter.Frame(master)
        attribute_label = tkinter.Label(attribute_frame, text=tag)
        self.attribute_value = tkinter.Entry(attribute_frame)
        self.attribute_value.insert(0, value)
        attribute_label.pack(fill=tkinter.X)
        self.attribute_value.pack(fill=tkinter.X)
        attribute_frame.pack(fill=tkinter.X)
        self.attribute_type = "int"

    def value_as_tags(self):
        inner_part = create_tag(self.tag, self.attribute_value.get())
        return create_tag("int", inner_part)

    def test_entry_legal(self):
        return self.attribute_value.get().isnumeric()




class ListOfStringsAttributeWidget:
    pass


class FileAttributeWidget:
    pass


class ListOfFilesAttributeWidget:
    pass


class EditorState:
    initial_directory = sys.path[1] + "/resources"

    def __init__(self):
        self.root = tkinter.Tk()
        self.mode = Mode.card
        self.current_file_name = None

        self.top_row = tkinter.Frame(self.root)
        self.top_row.grid(row=0)

        self.main_fields = tkinter.Frame(self.root)
        self.main_fields.grid(row=1)
        open_file_button = tkinter.Button(self.top_row, text="Open File", command=self.open_file)
        open_file_button.grid(column=0, row=0)

        save_button = tkinter.Button(self.top_row, text="Save", command=self.save)
        save_button.grid(column=3, row=0)

        save_button = tkinter.Button(self.top_row, text="Save As", command=self.save_as)
        save_button.grid(column=3, row=0)

        new_card_button = tkinter.Button(self.top_row, text="New Card", command=self.new_card)
        new_card_button.grid(column=1, row=0)

        new_character_button = tkinter.Button(self.top_row, text="New Character", command=self.new_character)
        new_character_button.grid(column=2, row=0)

    def clear_fields(self):
        for child in self.main_fields.winfo_children():
            child.destroy()
        Widget.flush()

    def set_main_fields(self):
        self.clear_fields()
        for tag, attribute_type in attributes_by_mode[self.mode].items():
            if attribute_type == "string":
                StringAttributeWidget(self.main_fields, tag, "")
            if attribute_type == "int":
                IntAttributeWidget(self.main_fields, tag, "")

    def set_main_fields_from_str(self, string: str):
        self.clear_fields()
        list_of_tags_and_values = list_tags_and_values(string)
        # for tag_pair in list_of_tags_and_values:
        #    create_widget_from_string(*tag_pair)

    def open_file(self):

        self.current_file_name = fd.askopenfilename(initialdir=EditorState.initial_directory)

        if not path.exists(self.current_file_name):
            return

        with open(self.current_file_name, "r") as file:
            file_content = file.read()

        self.set_main_fields_from_str(file_content)

    def state_to_string(self) -> str:
        result = ""
        for child in self.main_fields.winfo_children():
            result += str(child)
        return result

    def new_card(self):
        self.current_file_name = None
        self.mode = Mode.card
        self.set_main_fields()

    def new_character(self):
        self.current_file_name = None
        self.mode = Mode.person
        self.set_main_fields()

    def save(self):
        if not path.exists(self.current_file_name):
            return self.please_use_save_as()
        with open(self.current_file_name, "w") as file:
            file.write(self.state_to_string())

    def save_as(self):
        with fd.asksaveasfile(initialdir=EditorState.initial_directory, initialfile=self.current_file_name,
                              defaultextension=file_extension_by_mode[self.mode]) as file:
            file.write(self.state_to_string())

    @staticmethod
    def please_use_save_as():
        mb.showwarning("No file selcted", "Please select a file to save to using Save As")


def main():

    Editor = EditorState()





    Editor.set_main_fields()

    Editor.root.mainloop()


def create_widget_from_string(type: str, string: str):
    if type == "string":
        return StringAttributeWidget(*(list_tags_and_values(string)[0]))



if __name__ == "__main__":
    main()

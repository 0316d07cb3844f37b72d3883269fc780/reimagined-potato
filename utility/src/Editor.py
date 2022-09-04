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

    def test_entry_legal(self):
        pass


class StringAttributeWidget(Widget):

    def __init__(self, master, tag, value):
        super().__init__()
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
        entry = self.attribute_value.get()
        list_of_strings = entry.split("\n")
        inner_part = create_tag(self.tag, list_of_strings)
        return create_tag("int", inner_part)


class FileAttributeWidget:
    def __init__(self, master, tag, value):
        self.tag = tag
        attribute_frame= tkinter.Frame(master)
        self.tag_label = tkinter.Label(attribute_frame, text=tag)
        self.tag_label.pack(fill=tkinter.X)
        value_frame = tkinter.Frame(attribute_frame)
        value_editor = EditorState(super_editor_frame=value_frame)

        self.update_tag_label()

    def update_tag_label(self):
        self.tag_label.after(self.update_tag_label())


class ListOfFilesAttributeWidget:
    pass


class EditorState:
    initial_directory = sys.path[1] + "/resources"

    def __init__(self, super_editor_frame=None, current_file_name =None):

        if super_editor_frame is None:
            self.root = tkinter.Tk()
        else:
            self.root = super_editor_frame

        self.mode = Mode.card
        self.current_file_name = current_file_name
        self.widgets = []

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

        if current_file_name is not None:
            with open(self.current_file_name, "r") as file:
                file_content = file.read()

            self.set_main_fields_from_str(file_content)

    def clear_fields(self):
        for child in self.main_fields.winfo_children():
            child.destroy()
        self.widgets = []

    def set_main_fields(self):
        self.clear_fields()
        for tag, attribute_type in attributes_by_mode[self.mode].items():
            if attribute_type == "string":
                self.widgets += StringAttributeWidget(self.main_fields, tag, "")
            if attribute_type == "int":
                self.widgets += IntAttributeWidget(self.main_fields, tag, "")

    def set_main_fields_from_str(self, string: str):
        self.clear_fields()
        dict_of_tags_and_values = dict(list_tags_and_values(string))
        for tag, attribute_type in attributes_by_mode[self.mode].items():
            pass

    def open_file(self):

        self.current_file_name = fd.askopenfilename(initialdir=EditorState.initial_directory)

        if not path.exists(self.current_file_name):
            return

        with open(self.current_file_name, "r") as file:
            file_content = file.read()

        self.set_main_fields_from_str(file_content)

    def state_to_string(self) -> str:
        result = ""
        for child in self.widgets:
            result += child.value_as_tags()
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

    def check_widget_entries_are_legal(self):
        return [widget.test_entry_legal() for widget in self.widgets].all()


    @staticmethod
    def please_use_save_as():
        mb.showwarning("No file selected", "Please select a file to save to using Save As")


def main():
    editor = EditorState()

    editor.set_main_fields()

    editor.root.mainloop()


def create_widget_from_string(attribute_type: str, string: str):
    if type == "string":
        return StringAttributeWidget(*(list_tags_and_values(string)[0]))


if __name__ == "__main__":
    main()

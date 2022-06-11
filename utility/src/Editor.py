import sys
import tkinter
import tkinter.filedialog as fd
from enum import Enum
from os import path

from string_utils import *


class Mode(Enum):
    card = 0
    person = 1
    team = 1


file_extension_by_mode = {
    Mode.card: ".card",
    Mode.person: ".person",
    Mode.team: ".team"
}

mode_by_file_extension={}
for mode, extension in file_extension_by_mode.items():
    mode_by_file_extension[extension]=mode


attributes_by_mode = {
    Mode.card: {
        "name": "string",
        "action_factory": "string",
        "speed": "string",
        "target_checker": "string",
        "image": "string"
    }
}

file_types = (("Card File", "*.card"),
              ("Person File", "*.person"))


def main():
    class EditorState:
        pass

    state = EditorState()
    root = tkinter.Tk()
    state.mode = Mode.card
    state.current_file_name = None

    top_row = tkinter.Frame(root)
    top_row.grid(row=0)

    main_fields = tkinter.Frame(root)
    main_fields.grid(row=1)

    test_label = tkinter.Label(main_fields, text="test")
    test_label.pack()

    class AttributeWidget:
        def __init__(self, tag, value):
            self.tag = tag
            attribute_frame = tkinter.Frame(main_fields)
            attribute_label = tkinter.Label(attribute_frame, text=tag)
            self.attribute_value = tkinter.Entry(attribute_frame)
            self.attribute_value.insert(0, value)
            attribute_label.pack(fill=tkinter.X)
            self.attribute_value.pack(fill=tkinter.X)
            attribute_frame.pack(fill=tkinter.X)

        def __str__(self):
            return create_tag(self.tag, self.attribute_value.get())

    def set_main_fields():
        for child in main_fields.winfo_children():
            child.destroy()
        for tag, attribute_type in attributes_by_mode[state.mode].items():
            if attribute_type == "string":
                AttributeWidget(tag, "")

    def set_main_fields_from_str(string: str):
        for child in main_fields.winfo_children():
            child.destroy()
        list_of_tags_and_values = list_tags_and_values(string)
        for tag_pair in list_of_tags_and_values:
            AttributeWidget(*tag_pair)

    def open_file():

        state.current_file_name = fd.askopenfilename(initialdir=sys.path[1] + "/resources")

        if not path.exists(state.current_file_name):
            return

        with open(state.current_file_name, "r") as file:
            file_content = file.read()
            file.close()

        set_main_fields_from_str(file_content)

    def state_to_string() -> str:
        result = ""
        for child in main_fields.winfo_children():
            result += str(child)
        return result

    def new_card():
        state.current_file = None
        state.mode = Mode.card
        set_main_fields()

    def new_character():
        state.current_file = None
        state.mode = Mode.person
        set_main_fields()

    def save():
        if not path.exists(state.current_file_name):
            return
        with open(state.current_file_name,"w") as file:
            file.write(state_to_string())

    def save_as():
        pass

    open_file_button = tkinter.Button(top_row, text="Open File", command=open_file)
    open_file_button.grid(column=0, row=0)

    save_button = tkinter.Button(top_row, text="Save", command=save)
    save_button.grid(column=3, row=0)

    save_button = tkinter.Button(top_row, text="Save As", command=save_as)
    save_button.grid(column=3, row=0)

    new_card_button = tkinter.Button(top_row, text="New Card", command=new_card)
    new_card_button.grid(column=1, row=0)

    new_character_button = tkinter.Button(top_row, text="New Character", command=new_character)
    new_character_button.grid(column=2, row=0)

    set_main_fields()

    root.mainloop()


if __name__ == "__main__":
    main()
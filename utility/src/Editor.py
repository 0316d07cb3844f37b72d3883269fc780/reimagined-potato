import sys
import tkinter
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from enum import Enum
from os import path

from utility.src.string_utils import *


class Mode(Enum):
    card = 0
    person_base = 1
    person_fighting = 2
    team = 3
    scene = 4


class AttributeType(Enum):
    string = 0
    int = 1
    file = 2
    cards = 3
    person_base = 4
    people = 5


file_extension_by_mode = {
    Mode.card: ".card",
    Mode.person_base: ".person",
    Mode.team: ".team"
}

mode_by_file_extension = {}
for mode, extension in file_extension_by_mode.items():
    mode_by_file_extension[extension] = mode

attributes_by_mode = {
    Mode.card: {
        "name": AttributeType.string,
        "action_factory": AttributeType.string,
        "speed": AttributeType.string,
        "target_checker": AttributeType.string,
        "image": AttributeType.string
    },

    Mode.person_base: {

    },

    Mode.team: {

    }
}

file_types = (("Card File", "*.card"),
              ("Person File", "*.person"))


class Widget:

    def test_entry_legal(self):
        pass

    def save(self):
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
        return create_tag(self.tag, self.attribute_value.get())


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


class ListOfStringsAttributeWidget(Widget):
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


class List_item_widget(Widget):
    def __init__(self, master, widget_list):
        self.widget_list = widget_list
        self.main_frame = tkinter.Frame(master, relief="sunken")
        self.top_row_frame = tkinter.Frame(master)
        self.widget_frame = tkinter.Frame(master)
        self.top_row_frame.pack(), self.widget_frame.pack()
        self.index = None
        self.contained_widget = None
        for command, text in [(self.add_item, "Add item above"), (self.move_up, "Move Up"), (self.add_item, "Add above")]:
            new_button=tkinter.Button(master=self.top_row_frame, command=command, text=text)
            new_button.pack()

    def move_up(self):
        self.widget_list.move_widget_up(self.get_index())

    def delete_from_list(self):
        self.widget_list.delete_from_list(self.get_index())

    def add_item(self):
        self.widget_list.add_item(self.get_index())

    def get_index(self):
        self.widget_list.set_indices()
        return self.index

    def value_as_tags(self):
        return self.contained_widget.value_as_tags


class FileAttributeWidget(Widget):
    def __init__(self, master, tag, value, restriction=Mode.card):
        self.tag = tag
        attribute_frame = tkinter.Frame(master)
        self.tag_label = tkinter.Label(attribute_frame, text=tag)
        value_frame = tkinter.Frame(attribute_frame)
        self.value_editor = EditorState(super_editor_frame=value_frame, current_file_name=value,
                                        starting_mode=restriction)
        for widget in [attribute_frame, self.tag_label, value_frame]:
            widget.pack(fill=tkinter.X)
        self.update_tag_label()

    def value_as_tags(self):
        value = self.value_editor.current_file_name
        return create_tag("file", value)

    def update_tag_label(self):
        self.tag_label.configure(text=self.value_editor.current_file_name)
        self.tag_label.after(16, func=self.update_tag_label)

    def save(self):
        self.value_editor.save()


class ListOfFilesAttributeWidget(Widget):
    def __init__(self, master, tag, value: str, file_type_restriction=None):
        self.tag = tag
        self.file_type_restriction = None
        main_frame = tkinter.Frame(master)
        main_frame.pack()
        self.tag_label = tkinter.Label(main_frame, text=tag)
        self.files_frame = tkinter.Frame(main_frame)
        self.list_of_filenames = [detag_given_tags(tagged_entry, "file")[0] for tagged_entry in value.split(",")]
        self.list_items = [List_item_widget(self.files_frame, self) for name in self.list_of_filenames]
        self.list_of_file_widgets = [FileAttributeWidget(list_item.widget_frame, self.tag, name) for list_item, name in
                                     zip(self.list_items, self.list_of_filenames)]
        for list_item, file_widget in zip(self.list_items, self.list_of_file_widgets):
            list_item.contained_widget = file_widget
        self.repack()
        self.bottom_row = tkinter.Frame(main_frame)

    @classmethod
    def get_restricted_constructor(cls, restriction):
        return lambda *arguments: ListOfFilesAttributeWidget(*arguments, file_type_restriction=restriction)

    def add_file_attribute_widget(self, file_name):
        new_list_item_widget = List_item_widget(self.files_frame, self)
        self.list_items.append(new_list_item_widget)

    def value_as_tags(self):
        value_of_list_items = ", ".join([item.value_as_tags() for item in self.list_items])
        return create_tag(self.tag, value_of_list_items)

    def move_widget_up(self, index):
        if index > 0:
            self.list_items[index - 1], self.list_items[index] = self.list_items[index], self.list_items[index - 1]
        self.repack()

    def delete_from_list(self, index):
        self.list_items.pop(index)
        self.repack()

    def add_item(self, index):
        new_list_item = List_item_widget(self.files_frame, self)
        new_file_widget = FileAttributeWidget(new_list_item.widget_frame, self.tag, value=None,
                                              restriction=self.file_type_restriction)
        new_list_item.contained_widget=new_file_widget
        self.list_of_file_widgets.insert(index, new_file_widget)
        self.repack()

    def repack(self):
        for child in self.files_frame.winfo_children():
            child.pack_forget()
        for list_item in self.list_items:
            list_item.widget_frame.pack()

    def set_indices(self):
        for i, list_item in enumerate(self.list_items):
            list_item.index = i

    def save(self):
        for child in self.list_items:
            child.save()


widget_by_attribute_type = {
    AttributeType.string: StringAttributeWidget,
    AttributeType.int: IntAttributeWidget,
    AttributeType.file: ListOfFilesAttributeWidget,
    AttributeType.cards: ListOfFilesAttributeWidget.get_restricted_constructor(Mode.card)
}


class EditorState:
    initial_directory = sys.path[0] + "/../../resources/"

    def __init__(self, super_editor_frame=None, current_file_name=None, starting_mode=Mode.card):

        if super_editor_frame is None:
            self.root = tkinter.Tk()
        else:
            self.root = super_editor_frame

        self.mode = starting_mode
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
        self.set_main_fields_from_str("")

    def set_main_fields_from_str(self, string: str):
        self.clear_fields()
        dict_of_tags_and_values = dict(list_tags_and_values(string))
        for tag, attribute_type in attributes_by_mode[self.mode].items():
            initial_value = dict_of_tags_and_values.get(tag, "")
            self.widgets.append(widget_by_attribute_type[attribute_type](self.main_fields, tag, initial_value))

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
        self.mode = Mode.person_base
        self.set_main_fields()

    def save(self):
        if not path.exists(self.current_file_name):
            return self.please_use_save_as()
        with open(self.current_file_name, "w") as file:
            file.write(self.state_to_string())
        for widget in self.widgets:
            widget.save()

    def save_as(self):
        with fd.asksaveasfile(initialdir=EditorState.initial_directory, initialfile=self.current_file_name,
                              defaultextension=file_extension_by_mode[self.mode]) as file:
            file.write(self.state_to_string())
        for widget in self.widgets:
            widget.save()

    def check_widget_entries_are_legal(self):
        return all([widget.test_entry_legal() for widget in self.widgets])

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

import sys
import tkinter
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from enum import Enum, auto, IntFlag
from os import path

from utility.src.string_utils import *


class Mode(Enum):
    card = auto(IntFlag)
    card_collection = auto(IntFlag)
    person_base = auto(IntFlag)
    person_fighting = auto(IntFlag)
    team = auto(IntFlag)
    scene = auto(IntFlag)


class AttributeType(Enum):
    string = auto(IntFlag)
    int = auto(IntFlag)
    single_file = auto(IntFlag)
    files_list = auto(IntFlag)
    cards = auto(IntFlag)
    card_collection = auto(IntFlag)
    person_base = auto(IntFlag)
    people = auto(IntFlag)
    deck = auto(IntFlag)
    team = auto(IntFlag)


file_extension_by_mode = {
    Mode.card: ".card",
    Mode.card_collection: ".collection",
    Mode.person_base: ".person_base",
    Mode.person_fighting: ".person_fighting",
    Mode.team: ".team",
    Mode.scene: ".scene",

}

mode_by_file_extension = {}
for mode, extension in file_extension_by_mode.items():
    mode_by_file_extension[extension] = mode

attributes_by_mode = {
    Mode.card: {
        "type": AttributeType.string,
        "name": AttributeType.string,
        "action_factory": AttributeType.string,
        "speed": AttributeType.string,
        "target_checker": AttributeType.string,
        "scene_id": AttributeType.string
    },

    Mode.card_collection: {
        "cards": AttributeType.cards,
    },

    Mode.person_base: {
        "max_health": AttributeType.int,
        "health": AttributeType.int,
        "deck": AttributeType.deck,
        "scene_id": AttributeType.string,
        "person_type": AttributeType.string,

    },

    Mode.person_fighting: {
        "base_person": AttributeType.person_base,
        "drapile": AttributeType.card_collection,
        "hand": AttributeType.card_collection,
        "discardpile": AttributeType.card_collection,
        "scene_id": AttributeType.string,

    },

    Mode.team: {
        "team": AttributeType.team
    },

    Mode.scene: {

    },

}

file_types = (("Card File", "*.card"),
              ("Collection File", "*.collection"),
              ("Person Base File", "*.person_base"),
              ("Person Fighting File", "*.person_fighting"),
              ("Team File", ".team"),
              ("Scene File", ".scene")
              )


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
        attribute_label.pack(side=tkinter.TOP)
        self.attribute_value.pack(side=tkinter.BOTTOM)
        attribute_frame.pack(side=tkinter.BOTTOM)
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
        attribute_label.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.attribute_value.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        attribute_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
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


class ListItemWidget(Widget):
    def __init__(self, master, widget_list):
        self.widget_list = widget_list
        self.main_frame = tkinter.Frame(master, relief="sunken")
        self.top_row_frame = tkinter.Frame(master)
        self.widget_frame = tkinter.Frame(master)
        self.top_row_frame.pack(), self.widget_frame.pack()
        self.index = None
        self.contained_widget = None
        for command, text in [(self.add_item, "Add item above"), (self.move_up, "Move Up"),
                              (self.add_item, "Add above")]:
            new_button = tkinter.Button(master=self.top_row_frame, command=command, text=text)
            new_button.pack(side=tkinter.RIGHT)

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
        return self.contained_widget.value_as_tags()


class DeckAttributeWidget(Widget):

    def __init__(self, master, tag, value):
        super().__init__()
        self.tag = tag
        attribute_frame = tkinter.Frame(master)
        attribute_label = tkinter.Label(attribute_frame, text=tag)
        self.attribute_value = tkinter.Text(attribute_frame)
        self.attribute_value.insert(0, value)
        attribute_label.pack(fill=tkinter.X)
        self.attribute_value.pack(fill=tkinter.X)
        attribute_frame.pack(fill=tkinter.X)
        self.attribute_type = "string"

    def value_as_tags(self):
        field_content = self.attribute_value.get("1.0", "end-1c")
        content_as_list = field_content.split("\n")
        content_as_list = [create_tag("card", line) for line in content_as_list]
        result = "\n".join(content_as_list)
        return create_tag(self.tag, result)


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

    @classmethod
    def get_custom_constructor(cls, restriction: Mode):
        return lambda *arguments: FileAttributeWidget(*arguments, restriction=restriction)

    def value_as_tags(self):
        value = self.value_editor.current_file_name
        return create_tag("file", value)

    def update_tag_label(self):
        self.tag_label.configure(text=self.value_editor.current_file_name)
        self.tag_label.after(16, func=self.update_tag_label)

    def save(self):
        self.value_editor.save()


class ListOfFilesAttributeWidget(Widget):
    def __init__(self, master, tag, value: str, file_type_restriction=None, elements_tag=None):
        self.tag = tag
        if elements_tag is None:
            self.elements_tag = tag
        self.file_type_restriction = file_type_restriction
        main_frame = tkinter.Frame(master)
        main_frame.pack()
        self.tag_label = tkinter.Label(main_frame, text=tag)
        self.files_frame = tkinter.Frame(main_frame)
        self.list_of_filenames = [detag_given_tags(tagged_entry, "file")[0] for tagged_entry in value.split(",")]
        self.list_items = [ListItemWidget(self.files_frame, self) for _ in self.list_of_filenames]
        self.list_of_file_widgets = [FileAttributeWidget(list_item.widget_frame, self.tag, name) for list_item, name in
                                     zip(self.list_items, self.list_of_filenames)]
        for list_item, file_widget in zip(self.list_items, self.list_of_file_widgets):
            list_item.contained_widget = file_widget
        self.scrollbar = tkinter.Scrollbar(self.files_frame, orient="vertical")
        self.repack()
        self.bottom_row = tkinter.Frame(main_frame)

    @classmethod
    def get_custom_constructor(cls, restriction: Mode, elements_tag: str):
        return lambda *arguments: ListOfFilesAttributeWidget(*arguments, file_type_restriction=restriction,
                                                             elements_tag=elements_tag)

    def add_file_attribute_widget(self):
        new_list_item_widget = ListItemWidget(self.files_frame, self)
        self.list_items.append(new_list_item_widget)
        FileAttributeWidget(new_list_item_widget.widget_frame, self.elements_tag, None,
                            restriction=self.file_type_restriction)

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
        new_list_item = ListItemWidget(self.files_frame, self)
        new_file_widget = FileAttributeWidget(new_list_item.widget_frame, self.tag, value=None,
                                              restriction=self.file_type_restriction)
        new_list_item.contained_widget = new_file_widget
        self.list_of_file_widgets.insert(index, new_file_widget)
        self.repack()

    def repack(self):
        for child in self.files_frame.winfo_children():
            child.pack_forget()
        for list_item in self.list_items:
            list_item.widget_frame.pack()
        self.scrollbar.pack(side="right", fill="y")

    def set_indices(self):
        for i, list_item in enumerate(self.list_items):
            list_item.index = i

    def save(self):
        for child in self.list_items:
            child.save()


class StaticInvisibleWidget(Widget):

    def __init__(self, _, tag, value):
        self.tag = tag
        self.value = value

    @classmethod
    def get_custom_constructor(cls, default_value: str):
        return lambda master, tag, value: StaticInvisibleWidget(master, tag, default_value)

    def get_value_as_tags(self):
        return create_tag(self.tag, self.value)


widget_by_attribute_type = {
    AttributeType.string: StringAttributeWidget,
    AttributeType.int: IntAttributeWidget,
    AttributeType.files_list: ListOfFilesAttributeWidget,
    AttributeType.cards: ListOfFilesAttributeWidget.get_custom_constructor(Mode.card, "card"),
    AttributeType.card_collection: FileAttributeWidget.get_custom_constructor(Mode.card_collection),
    AttributeType.deck: DeckAttributeWidget,
    AttributeType.single_file: FileAttributeWidget,
    AttributeType.person_base: FileAttributeWidget.get_custom_constructor(Mode.person_base),
    AttributeType.team: ListOfFilesAttributeWidget.get_custom_constructor(Mode.person_fighting, "fighter")


}


class EditorState:
    initial_directory = sys.path[0] + "/../../resources/"

    def __init__(self, super_editor_frame=None, current_file_name=None, starting_mode=Mode.card):

        if super_editor_frame is None:
            self.root_window = tkinter.Tk()
            main_frame = tkinter.Frame(self.root_window)
            main_frame.pack(fill="both", expand=1)
            my_canvas = tkinter.Canvas(main_frame)
            my_canvas.pack(side="left", fill="both", expand=1)
            my_scrollbar = tkinter.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
            my_scrollbar.pack(side="right", fill="y")
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
            self.root = tkinter.Frame(my_canvas)
            my_canvas.create_window((0, 0), window=self.root, anchor="nw")
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


if __name__ == "__main__":
    main()

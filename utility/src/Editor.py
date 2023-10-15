import tkinter
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from enum import Enum
from enum import auto as auto
from os import path

from utility.src.string_utils import *


class Mode(Enum):
    card = auto()
    card_collection = auto()
    person_base = auto()
    person_fighting = auto()
    team = auto()
    scene = auto()


class AttributeType(Enum):
    string = auto()
    int = auto()
    single_file = auto()
    files_list = auto()
    card = auto()
    cards = auto()
    card_collection = auto()
    location = auto()
    person_base = auto()
    people = auto()
    deck = auto()
    team_internal = auto()
    team = auto()
    action_empty = auto()
    stance_empty = auto()
    turn_side_allies = auto()
    empty = auto()


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
        "card_type": AttributeType.string,
        "name": AttributeType.string,
        "action_factory": AttributeType.string,
        "speed": AttributeType.string,
        "target_checker": AttributeType.string,
        "location": AttributeType.location,
        "scene_id": AttributeType.string
    },

    Mode.card_collection: {
        "cards": AttributeType.cards,
        "scene_id": AttributeType.string,
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
        "actions": AttributeType.empty,
        "stances": AttributeType.empty,
        "resist": AttributeType.string,
        "turn_ended": AttributeType.string,
        "drawpile": AttributeType.card_collection,
        "hand": AttributeType.card_collection,
        "discardpile": AttributeType.card_collection,
        "scene_id": AttributeType.string,

    },

    Mode.team: {
        "team": AttributeType.team_internal
    },

    Mode.scene: {
        "allies": AttributeType.team,
        "foes": AttributeType.team,
        "turn_side": AttributeType.turn_side_allies,
        "actions": AttributeType.empty,
        "stances": AttributeType.empty,
        "card_in_resolution": AttributeType.empty,
        "targets_being_selected_ids": AttributeType.empty,
    },

}

file_types = (("Card File", "*.card"),
              ("Collection File", "*.collection"),
              ("Person Base File", "*.person_base"),
              ("Person Fighting File", "*.person_fighting"),
              ("Team File", "*.team"),
              ("Scene File", "*.scene")
              )

name_by_ending = dict([(ending.replace("*", ""), name) for name, ending in file_types])


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
        attribute_label.pack(side=tkinter.TOP, fill=tkinter.X)
        self.attribute_value.pack(side=tkinter.TOP, fill=tkinter.X)
        attribute_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        self.attribute_type = "string"

    def value_as_tags(self):
        return create_tag(self.tag, self.attribute_value.get())


class IntAttributeWidget(Widget):
    def __init__(self, master, tag, value):
        if tag == "int":
            reduce_bangs = value.replace("<!", "<")
            tag, value = list_tags_and_values(reduce_bangs)[0]
        self.tag = tag
        attribute_frame = tkinter.Frame(master)
        attribute_label = tkinter.Label(attribute_frame, text=tag)
        self.attribute_value = tkinter.Entry(attribute_frame)
        self.attribute_value.insert(0, value)
        attribute_label.pack(side=tkinter.TOP, fill=tkinter.X)
        self.attribute_value.pack(side=tkinter.TOP, fill=tkinter.X)
        attribute_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        self.attribute_type = "int"

    def value_as_tags(self):
        return create_tag(self.tag, self.attribute_value.get())
        # inner_part = create_tag(self.tag, self.attribute_value.get())
        # return create_tag("int", inner_part)

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
        self.main_frame.pack(side=tkinter.TOP)
        self.top_row_frame = tkinter.Frame(self.main_frame)
        self.widget_frame = tkinter.Frame(self.main_frame)
        self.top_row_frame.pack(side=tkinter.TOP)
        self.widget_frame.pack(side=tkinter.TOP)
        self.index = None
        self.contained_widget = None
        for command, text in [(self.add_item, "Add item above"), (self.move_up, "Move Up"),
                              (self.delete_from_list, "Delete Me")]:
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
        self.attribute_value.insert(tkinter.INSERT, value)
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
        file_name, = detag_given_tags(value, "file")
        if file_name != "":
            self.value_editor = EditorState(super_editor_frame=value_frame, file_name=file_name,
                                            mode_restriction=restriction)
        else:
            self.value_editor = EditorState(super_editor_frame=value_frame, file_name=None,
                                            mode_restriction=restriction)
            if value != "":
                self.value_editor.set_main_fields_from_str(value)

        for widget in [attribute_frame, self.tag_label, value_frame]:
            widget.pack(side=tkinter.TOP, fill=tkinter.X)
        self.update_tag_label()

    @classmethod
    def get_custom_constructor(cls, restriction: Mode):
        return lambda *arguments: FileAttributeWidget(*arguments, restriction=restriction)

    def value_as_tags(self):
        value = self.value_editor.current_file_name
        return create_tag("file", unroot_path(value))

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
        else:
            self.elements_tag = elements_tag
        self.file_type_restriction = file_type_restriction
        self.main_frame = tkinter.Frame(master)
        self.tag_label = tkinter.Label(self.main_frame, text=tag)
        self.files_frame = tkinter.Frame(self.main_frame)
        self.tag_label.pack(side=tkinter.TOP)

        if value == "":
            self.list_of_filenames = []
            self.list_items = [ListItemWidget(self.files_frame, self)]
            self.list_of_file_widgets = [FileAttributeWidget(self.list_items[0].widget_frame, self.elements_tag, "",
                                                             restriction=file_type_restriction)]
            self.list_items[0].contained_widget = self.list_of_file_widgets[0]
        else:
            self.list_of_filenames = [detag_given_tags(tagged_entry, "file")[0] for tagged_entry in value.split(",")]
            self.list_items = [ListItemWidget(self.files_frame, self) for _ in self.list_of_filenames]
            self.list_of_file_widgets = [
                FileAttributeWidget(list_item.widget_frame, self.elements_tag, name, restriction=file_type_restriction)
                for
                list_item, name in
                zip(self.list_items, self.list_of_filenames)]
            for list_item, file_widget in zip(self.list_items, self.list_of_file_widgets):
                list_item.contained_widget = file_widget
        self.files_frame.pack(side=tkinter.TOP, )
        self.repack()
        self.bottom_row = tkinter.Frame(self.main_frame)
        self.main_frame.pack()

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
        new_file_widget = FileAttributeWidget(new_list_item.widget_frame, self.tag, value="",
                                              restriction=self.file_type_restriction)
        new_list_item.contained_widget = new_file_widget
        self.list_items.insert(index, new_list_item)
        self.list_of_file_widgets.insert(index, new_file_widget)
        self.repack()

    def repack(self):
        for child in self.files_frame.winfo_children():
            child.pack_forget()
        for list_item in self.list_items:
            list_item.main_frame.pack(side=tkinter.TOP, )

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

    def value_as_tags(self):
        return create_tag(self.tag, self.value)


widget_by_attribute_type = {
    AttributeType.string: StringAttributeWidget,
    AttributeType.int: IntAttributeWidget,
    AttributeType.files_list: ListOfFilesAttributeWidget,
    AttributeType.card: FileAttributeWidget.get_custom_constructor(Mode.card),
    AttributeType.cards: ListOfFilesAttributeWidget.get_custom_constructor(Mode.card, "card"),
    AttributeType.card_collection: FileAttributeWidget.get_custom_constructor(Mode.card_collection),
    AttributeType.location: StaticInvisibleWidget.get_custom_constructor(""),
    AttributeType.deck: DeckAttributeWidget,
    AttributeType.single_file: FileAttributeWidget,
    AttributeType.person_base: FileAttributeWidget.get_custom_constructor(Mode.person_base),
    AttributeType.team_internal: ListOfFilesAttributeWidget.get_custom_constructor(Mode.person_fighting, "fighter"),
    AttributeType.team: FileAttributeWidget.get_custom_constructor(Mode.team),
    AttributeType.turn_side_allies: StaticInvisibleWidget.get_custom_constructor("allies"),
    AttributeType.empty: StaticInvisibleWidget.get_custom_constructor(""),

}


class EditorState:
    initial_directory = ROOT + "/resources/"

    def __init__(self, super_editor_frame=None, file_name=None, mode_restriction=None):

        if super_editor_frame is None:
            self.root_window = tkinter.Tk()
            main_frame = tkinter.Frame(self.root_window)
            main_frame.pack(fill="both", expand=1)
            self.my_canvas = tkinter.Canvas(main_frame, confine=False)
            self.my_canvas.pack(side="left", fill="both", expand=1)
            my_scrollbar = tkinter.Scrollbar(main_frame, orient="vertical", command=self.my_canvas.yview)
            my_scrollbar.pack(side="right", fill="y")
            self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
            self.my_canvas.bind('<Configure> <Button-1>',
                                lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
            self.root = tkinter.Frame(self.my_canvas)
            self.root.bindtags(("all",))
            self.my_canvas.create_window((0, 0), window=self.root, anchor="nw")
        else:
            self.root = super_editor_frame
        if mode_restriction is None:
            self.mode = Mode.card
        else:
            self.mode = mode_restriction
        self.current_file_name = root_path(file_name)
        self.widgets = []

        self.top_row = tkinter.Frame(self.root)
        self.top_row.grid(row=0)

        self.main_fields = tkinter.Frame(self.root)
        self.main_fields.grid(row=1)
        open_file_button = tkinter.Button(self.top_row, text="Open File", command=self.open_file)
        open_file_button.grid(column=0, row=0)

        if mode_restriction is None:
            relevant_modes = list(Mode)
        else:
            relevant_modes = [mode_restriction]

        for i, next_mode in enumerate(relevant_modes, start=1):
            mode_text = "New " + name_by_ending[file_extension_by_mode[next_mode]]
            command = self.new_file(next_mode)
            new_button = tkinter.Button(self.top_row, text=mode_text, command=command)
            new_button.grid(column=i, row=0)

        save_button = tkinter.Button(self.top_row, text="Save", command=self.save)
        save_button.grid(column=len(Mode) + 1, row=0)

        save_button = tkinter.Button(self.top_row, text="Save As", command=self.save_as)
        save_button.grid(column=len(Mode) + 2, row=0)

        if file_name is not None:
            with open(self.current_file_name, "r") as file:
                file_content = file.read()

            self.set_main_fields_from_str(file_content)
        else:
            self.set_main_fields()

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
        self.root.update()
        if hasattr(self, "my_canvas"):
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

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
            result += child.value_as_tags() + "\n"
        return result

    def new_file(self, my_mode: Mode) -> callable:
        def my_callable():
            self.current_file_name = None
            self.mode = my_mode
            self.set_main_fields()

        return my_callable

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

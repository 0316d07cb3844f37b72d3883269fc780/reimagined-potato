import tkinter
import tkinter.filedialog as fd
from enum import Enum
from os import path
import sys


class Mode(Enum):
    card = 0
    person = 1
    team = 1

file_extension_by_mode={
    Mode.card: ".card",
    Mode.person: ".person",
    Mode.team: ".team"
}

attributes_by_mode={
    Mode.card : {
        "name": "string",
        "action_factory":"string",
        "speed":"string",
        "target_checker":"string",
        "image":"string"
    }
}


def main():
    root = tkinter.Tk()
    mode=Mode.card
    current_file_name=None

    top_row =tkinter.Frame(root)
    top_row.grid(row=0)

    main_fields=tkinter.Frame(root)
    main_fields.grid(row=1)

    class Attribute_Widget():
        def __init__(self, tag, value):
            self.tag=tag
            attribute_frame = tkinter.Frame(main_fields)
            attribute_label = tkinter.Label(attribute_frame, text=tag)
            attribute_value = tkinter.Entry(attribute_frame).insert(0,value)
            attribute_value.pack(fill=tkinter.X)
            attribute_label.pack(fill=tkinter.X)
            attribute_frame.pack(fill=tkinter.X)

    def set_main_fields():
        for child in main_fields.winfo_children():
            child.destroy()
        for tag, type in attributes_by_mode[mode]:
            if type=="string":
                Attribute_Widget(tag,"")
                break

    def select_file():
        file_types=(("Card File", "*.card"),
                    ("Person File", "*.person"))

        current_file_name=fd.askopenfilename(initialdir=sys.path[1]+"/resources")

        if not path.exists(current_file_name):
            return

        file=open(current_file_name, "r")

        file.close()

    def new_card():
        current_file=None
        mode=Mode.card

    def new_character():
        current_file=None
        mode=Mode.person

    def save():
        pass

    open_file_button=tkinter.Button(top_row,text="Open File",command=select_file)
    open_file_button.grid(column=0, row=0)

    new_card_button=tkinter.Button(top_row, text="New Card", command=new_card)
    new_card_button.grid(column=1, row=0)

    new_character_button=tkinter.Button(top_row, text="New Character", command=new_character)
    new_character_button.grid(column=2, row=0)

    save_button=tkinter.Button(top_row, text="Save", command=save)
    save_button.grid(column=3, row=0)

    set_main_fields()




    root.mainloop()


if __name__ == "__main__":
    main()

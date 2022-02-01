import tkinter
import tkinter.filedialog
from enum import Enum

class Mode(Enum):
    card=0
    person=1
    team=1


if __name__=="__main__":
    root = tkinter.Tk()
    root.mainloop()
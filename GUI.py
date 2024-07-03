from tkinter import *
import sys
from tkinter import filedialog


class GUI:
    def __init__(self, window, name, debugging=False):
        self.toggle_state = False
        self.project = ""
        self.tk = window
        self.canvas = Canvas(bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        tk = self.tk
        tk.title(name)

        menuBar = Menu(tk)
        tk.config(menu=menuBar)

        tk.bind_all("<Control-n>", None)
        tk.bind_all("<Control-o>", lambda x: self.dialog("openFile"))
        tk.bind_all("<Control-s>", lambda x: self.dialog("save"))
        tk.bind_all("<Control-S>", lambda x: self.dialog("saveAs"))
        tk.bind_all("<Control-q>", sys.exit)

        tk.bind_all("<Control-z>", None)
        tk.bind_all("<Control-y>", None)

        tk.bind("<F11>", self.fullscreen)

        tk.bind_all("<Control-h>", None)

        fileTab = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="File", menu=fileTab)
        fileTab.add_command(label="New", command=None, accelerator="Ctrl+N")
        fileTab.add_command(label="Open", command=lambda: self.dialog("openFile"), accelerator="Ctrl+O")
        fileTab.add_command(label="Save", command=lambda: self.dialog("save"), accelerator="Ctrl+S")
        fileTab.add_command(label="Save As", command=lambda: self.dialog("saveAs"), accelerator="Ctrl+Shift+S")
        fileTab.add_separator()
        fileTab.add_command(label="Exit", command=sys.exit, accelerator="Ctrl+Q")

        editTab = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="Edit", menu=editTab)
        editTab.add_command(label="Undo", command=None, accelerator="Ctrl+Z")
        editTab.add_command(label="Redo", command=None, accelerator="Ctrl+Y")

        viewTab = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="View", menu=viewTab)
        viewTab.add_command(label="Fullscreen", command=self.fullscreen, accelerator="F11")

        helpTab = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label="Help", menu=helpTab)
        helpTab.add_command(label="Help", command=None, accelerator="Ctrl+H")
        helpTab.add_command(label="About", command=None)

    def fullscreen(self, event=None):
        self.toggle_state = not self.toggle_state
        self.tk.attributes('-fullscreen', self.toggle_state)

    def dialog(self, action):
        if action == "openFile":
            self.project = filedialog.askopenfilename(filetypes=[("Meow File", "*.meow")])
            self.fileEvent('r')
        elif 'save' in action:
            if action == "saveAs" or self.project == "":
                self.project = filedialog.asksaveasfilename(filetypes=[("Meow File", "*.meow")])
                self.fileEvent('w')
            # code
        print(self.project)

    def fileEvent(self, mode):
        pass


if __name__ == "__main__":
    root = Tk()
    Application = GUI(root, "GUI")
    Application.tk.mainloop()

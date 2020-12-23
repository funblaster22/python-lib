from tkinter import *
tk = Tk()
list1 = Listbox(tk)
for i in range(5):
    list1.insert(i, str(i))
list1.pack()

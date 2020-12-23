import json
from tkinter import *
from tkinter import messagebox
import online


def launch(URL):
    print(URL)
    #exec(online.access(URL))


def context(event):
    name = event.widget.cget('text')
    #del config['launcher'][name]
    #print(config)
    try:
        popup_menu.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup_menu.grab_release()


def new():
    if online.validate(textbox.get()):
        meta = online.access(textbox.get()).split(',')
        config['launcher'][meta[0]] = meta[1]  # read name and URL
        with open('config.json', 'w') as file:
            file.write(json.dumps(config, indent=2))
        for child in mainframe.winfo_children():
            child.destroy()
        reload()
    else:
        messagebox.showinfo("Invalid URL", "Please check and try again")


root = Tk()
root.wm_attributes("-topmost", True)
root.resizable(0, 0)
root.title("BETA launcher")
root.bind_all('<Return>', new)

popup_menu = Menu(root, tearoff=0)
popup_menu.add_command(label="Delete",
    command=print)

mainframe = Frame(root)
mainframe.grid(column=0, row=0)
#mainframe.update()
#mainframe.columnconfigure(0, weight=1)
#mainframe.rowconfigure(0, weight=1)
mainframe.pack(padx=50)


def reload():
    global textbox, config
    with open('config.json') as file:
        config = json.load(file)
        print(config)

    count = 0
    for key in config['launcher'].keys():
        meow = Label(mainframe, text=key)
        meow.grid(row=count, column=0)
        Button(mainframe, text='Launch!',
            command=lambda: launch(config['launcher'][key]) ).grid(row=count, column=1)
        meow.bind("<Button-3>", context)
        count += 1

    textbox = Entry(mainframe)
    textbox.insert(0, 'URL')
    textbox.grid(row=count, column=0)
    Button(mainframe, text='Add New', command=new).grid(row=count, column=1)

reload()
root.mainloop()

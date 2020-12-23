import json
from tkinter import *
from tkinter import messagebox
from urllib.error import *
from os import system, getcwd
import online


class Launcher:
    def __init__(self):
        self.root = Tk()
        self.root.wm_attributes("-topmost", True)
        self.root.resizable(0, 1)
        self.root.title("BETA launcher")
        self.root.bind_all('<Return>', self.new)
        self.root.geometry("200x200")  # default 184 by 104
        
        self.reload()
        self.root.mainloop()


    def launch(self):
        self.info()
        if not self.is_online:
            return None
        
        for line in self.program.split('\n'):
            if 'import' in line:
                module = line.split(' ')[1]
                print('Installing ' + module)
                system('pip install ' + module)
	
        try:
            print(self.program)
            with open('$TEMP.py', 'w') as file:
                file.write(self.program)
            system('python ' + getcwd() + '\\$TEMP.py')
            #exec(online.access(game_URL))
        except URLError as err:
            messagebox.showinfo("Offline", "Check your internet and try again")


    def delete(self):
        del self.config['launcher'][self.programChoice.get()]
        with open('config.json', 'w') as file:
            file.write(json.dumps(self.config, indent=2))
        self.reload()


    def new(self, event=None):
        if online.validate(self.textbox.get()):
            meta = online.access(self.textbox.get()).split(',')
            self.config['launcher'][meta[1]] = self.textbox.get()  # read name and URL
            with open('config.json', 'w') as file:
                file.write(json.dumps(self.config, indent=2))
            self.reload()
        else:
            messagebox.showinfo("Invalid URL", "Please check and try again")


    def info(self, *args):
        self.URL = self.config['launcher'][self.programChoice.get()]
        try:
            self.program = online.access(self.URL).replace('\r\n', '\n')
            self.is_online = True
            info = self.program.split(',')[2]
            self.description['text'] = info
        except URLError as err:
            messagebox.showinfo("Offline", "Check your internet and try again")
            self.is_online = False
        except HTTPError:
            messagebox.showinfo("404 Not Found", "Reenter the join URL you were sent")
            self.delete()


    def reload(self):
        for child in self.root.winfo_children():
            child.destroy()
        
        with open('config.json') as file:
            self.config = json.load(file)
        print(self.config)

        programs = []
        for key in self.config['launcher'].keys():
            programs.append(key)

        if len(programs) != 0:
            self.description = Label(self.root, text='no info provided', wraplength=200)
            
            self.programChoice = StringVar(self.root)  # list of possible programs
            self.programChoice.trace("w", self.info)
            self.programChoice.set(programs[0])
            dropdown = OptionMenu(self.root, self.programChoice, *programs)
            dropdown.pack()
            #print(programs)

            self.description.pack()

            mainframe = Frame(self.root)
            mainframe.columnconfigure(0, weight=1)
            mainframe.columnconfigure(1, weight=1)
            Button(mainframe, text='Launch!', command=self.launch).grid(row=0, column=0)
            Button(mainframe, text='Delete :(', command=self.delete).grid(row=0, column=1)
            mainframe.pack(fill='x')

        self.textbox = Entry(self.root)  # add new program
        self.textbox.insert(0, 'URL')
        self.textbox.pack(side='left')
        Button(self.root, text='Add New', command=self.new).pack(side='left')


app = Launcher()

import json
from tkinter import *
from tkinter import messagebox
from urllib.error import *
from os import system, getcwd
from os.path import isdir
import online
from zipfile import ZipFile


class Launcher:
    def __init__(self):
        self.root = Tk()
        self.root.wm_attributes("-topmost", True)
        self.root.resizable(0, 1)
        self.root.title("BETA launcher")
        self.root.geometry("200x100")  # default 184 by 104
        
        self.load()
        self.root.mainloop()


    def update(self):
        print('Downloading ' + self.programChoice.get() + '...')
        local_filename = online.download(self.program[2])  # save the URL in config to own folder
        print(local_filename)
        with ZipFile(local_filename, 'r') as archive:
            archive.extractall()
        with open('config.json', 'w') as file:
            file.write(json.dumps(self.config, indent=2))


    def launch(self):
        if self.program[1] < self.web_config[self.programChoice.get()][1] or not isdir(getcwd() + '\\' + self.programChoice.get()):  # compare versions and update
            if not self.is_online:  # not connected and not downloaded
                messagebox.showerror("Cannot Launch", "Must connect to Internet for download")
                return None
            self.config[self.programChoice.get()] = self.web_config[self.programChoice.get()]
            self.update()
        
        print('cd ' + getcwd() + '\\' + self.programChoice.get() + ' && ' + self.programChoice.get() + '.exe')
        system('cd ' + getcwd() + '\\' + self.programChoice.get() + ' && ' + self.programChoice.get() + '.exe')


    def info(self, *args):
        self.program = self.web_config[self.programChoice.get()]
        self.description['text'] = self.program[0]  # display info


    def load(self):
        with open('config.json') as file:
            self.config = json.load(file)
            self.web_config = self.config
        print(self.config)

        try:
            self.web_config = json.loads(online.access('http://www.funblaster22.tk/python/programs.json'))
            print(self.web_config)
            self.is_online = True
        except URLError as err:
            messagebox.showinfo("Offline", "Check your internet and try again")
            self.is_online = False
        
        programs = []
        for key in self.web_config.keys():
            programs.append(key)

        if len(programs) != 0:
            mainframe = Frame(self.root)
            mainframe.columnconfigure(0, weight=1)
            mainframe.columnconfigure(1, weight=1)

            self.description = Label(self.root, text='no info provided', wraplength=200)
            
            self.programChoice = StringVar(self.root)  # list of possible programs
            self.programChoice.trace("w", self.info)
            self.programChoice.set(programs[0])
            dropdown = OptionMenu(mainframe, self.programChoice, *programs)
            dropdown.grid(row=0, column=0)
            #print(programs)

            Button(mainframe, text='Launch!', command=self.launch).grid(row=0, column=1)
            mainframe.pack(fill='x')
            self.description.pack()


app = Launcher()

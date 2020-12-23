import sys
from tkinter import *
VERSION = sys.version.split(' ')[0]


def repl(globals=None, locals=None) -> None:
    print("Python {} Shell".format(VERSION))
    dirs = ['C:\\Users\\Amy\\Documents\\python',
            'C:\\Users\\Amy\\AppData\\Local\\Programs\\Python\\Python36\\lib']
    for path in dirs:
        sys.path.append(path)

    while True:
        try:
            statement = input(">>> ")
            if statement == '':
                continue
            while statement[-1] == ':' or statement[-1] == '\\' or statement[-1] == ';':
                statement += '\n    ' + input("... ")

            try:
                _ = eval(statement, globals, locals)
                print(_)
            except:
                exec(statement, globals, locals)
        except Exception as oops:
            print(type(oops).__name__ + ':', oops)


if __name__ == "__main__":
    repl()

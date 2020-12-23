from pydub import AudioSegment
from pydub.playback import play
from urllib.request import urlopen, urlretrieve
from urllib.error import *
import requests
import json
import io
import re

from tkinter import *
from tkinter.ttk import *


def validate(URL) -> bool:
    if 'http' not in URL:
        return False
        #return validate('http://' + URL)

    result = re.search("(http[s]?):\/\/(.+\.).+", URL)
    if result != None:
      try:
          urlopen(URL)
          return True
      except URLError:
          pass
    return False
    #return False if result == None else True


def access(directory, encoding='ascii') -> str:
    return urlopen(directory).read().decode(encoding).replace('\r\n', '\n')


def download(URL, filepath = None):
    #tk = Tk()
    label = Label(text="Downloading {}: {}%")
    progress = 0
    return urlretrieve(URL, filepath)[0]


def custom_lib(directory):
    temp = access(directory)
    __name__ = "module"
    exec(temp)
    __name__ = "__main__"


def PlaySound(directory, backup=None):  # https://stackoverflow.com/questions/43941716/how-to-play-mp3-from-bytes
    try:
        data = urlopen(directory).read()
        song = AudioSegment.from_file(io.BytesIO(data), format=directory.split('.')[-1].split('?')[0])  # TODO: messy (gets file extension)
    except URLError:
        if backup is None:
            raise FileNotFoundError('You are offline and no fallback provided')
        song = AudioSegment.from_file(backup, format=backup.split('.')[-1])

    play(song)


def CheckConnection() -> bool:
    try:
        urlopen('http://216.58.192.142', timeout=1)  # google
        return True
    except URLError:
        return False


'''if __name__ == "__main__":
    with open('config.json') as file:
        config = json.load(file)
    
    program = access(config['programURL'])
    print(program)
    exec(program)'''

import json
from urllib.request import urlopen, urlretrieve
from urllib.error import *

from lib import online

config = {'update': [""]}
try:
    with open("config.json") as file:
        config = json.load(file)
except FileNotFoundError:
    pass


def update(que):  # TODO: speed up
    status = 0
    if online.CheckConnection() is False:
        print("Could not connect to the internet.")
        return None

    for url in que:
        print('Checking for updates...')
        url = url.replace("?dl=0", "?dl=1")
        # TODO: dropbox not contain ?dl=1
        try:
            data = urlopen(url)
        except (HTTPError, URLError):
            print("Could not find the file:")
            print(url)
            print("Make sure the URL exists and is valid!\n")
            continue
        except ValueError:
            continue
        filename = url.split('/')[-1].split('?')[0]  # messy

        try:
            file = open(filename, 'rb')
        except FileNotFoundError:
            print("Downloading " + filename + " ...")
            urlretrieve(url, filename)  # TODO: PermissionError denied
            continue
            
        if data.read() != file.read():
            print("Updating " + filename + " ...")
            urlretrieve(url, filename)
            status += 1
            # TODO: loading bar?
        file.close()

    print("You are up to date!")
    return status


if __name__ == "__main__":
    update(config["update"])

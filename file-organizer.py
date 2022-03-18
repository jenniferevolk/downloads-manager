import os
import zipfile
from zipfile import BadZipfile
import shutil
import filecmp


def unzip(filename):
    destination = os.path.splitext(filename)[0]
    if os.path.isdir(destination):
        n = 2
        while os.path.isdir(f"{destination}({n})"):
            n = n + 1
        destination = f"{destination}({n})"
    os.mkdir(destination)
    try:
        with zipfile.ZipFile(filename, 'r') as zipObj:
            zipObj.extractall(destination)
    except BadZipfile:
        print(f"[-] ERROR bad zipfile {filename}")
    else:
        os.remove(filename)
        print(f"[+] Unzipped {filename} to {destination}")


def move(filename):
    extension = os.path.splitext(filename)[1][1:]
    if extension in file_type:
        destination = file_type[extension]
        if not os.path.isdir(destination):
            os.mkdir(destination)
            print(f"[+] created {destination} folder")

        if not os.path.isfile(f"{destination}/{filename}"):
            shutil.move(filename, destination)
            print(f"[+] moved {filename} to {destination}")
        else:
            duplicate = filecmp.cmp(filename, f"{destination}/{filename}", shallow=False)
            if duplicate:
                print(f"[+] already have {filename}")
                os.remove(filename)
            else:
                n = 2
                name = os.path.splitext(filename)[0]
                while os.path.isfile(f"{destination}/{file}({n}).{extension}"):
                    n = n + 1
                destination = f"{destination}/{name}({n}).{extension}"
                shutil.move(filename, destination)
                print(f"[+] moved {filename} to {destination}")
    else:
        print(f"[-]unknown file type {extension} for {filename}")


def filelist(path):
    objects = os.listdir(path)
    list_of_files = []
    for obj in objects:
        if os.path.isfile(obj):
            list_of_files.append(obj)
    return sorted(list_of_files)


data = {
    "Bins": ["exe"],
    "Docs": ["pdf", "doc", "docx", "txt"],
    "Gifs": ["gif"],
    "Pics": ["jpg", "png"],
    "3D": ["fbx"],
    "Movies": ["mp4"]
}

# create file type index
folders = list(data.keys())
file_type = {}
for folder in folders:
    for filetype in data[folder]:
        file_type[filetype] = folder

# get list of files
files = filelist(os.getcwd())

for file in files:
    if file[-4] == ".zip":
        unzip(file)
    else:
        move(file)

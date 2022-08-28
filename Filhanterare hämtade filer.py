import logging
import os
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move
from os import scandir, rename
from os.path import splitext, exists, join
from time import sleep

source_dir = r"C:/Users/nikla/Downloads"
dest_zip = r"C:/Users/nikla/Downloads/Zip"
dest_dokument = r"C:/Users/nikla/Downloads/Dokument"
dest_program = r"C:/Users/nikla/Downloads/Program"
dest_bilder = r"C:/Users/nikla/Downloads/Bilder"
dest_pdf = r"C:/Users/nikla/Downloads/PDF"


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class Filhanterare(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith(".zip"):
                    dest = dest_zip
                    move(dest, entry, name)
                elif name.endswith(".doc") or name.endswith(".txt"):
                    dest = dest_dokument
                    move(dest, entry, name)
                elif name.endswith(".exe"):
                    dest = dest_program
                    move(dest, entry, name)
                elif name.endswith(".jpg") or name.endswith(".png"):
                    dest = dest_bilder
                    move(dest, entry, name)
                elif name.endswith(".pdf"):
                    dest = dest_pdf
                    move(dest, entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = Filhanterare()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

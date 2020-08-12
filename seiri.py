#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# This script organizes files and directories in a custom catalogue.

import os
import sys
import collections
import tkinter
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import json
from pathlib import Path

tk = tkinter.Tk()
tk.withdraw()


class Music:
    extensions = [".wav", ".aif", ".mp3", ".flac"]


class Projects:
    extensions = [".als", ".logicx", ".ptx"]


class Code:
    extensions = [
        ".html", ".css", ".js", ".pug", ".scss", ".sass", ".md", ".py", ".php"
    ]


class Video:
    extensions = [".mp4", ".mov", ".prproj"]


class Photos:
    extensions = [".png", ".jpg", ".jpeg", ".gif", ".ttf", ".otf", ".woff"]


class Documents:
    extensions = [
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".rtfd", ".xml", ".odt"
    ]


class Utilities:
    extensions = [".dmg", ".iso", ".pkg", ".exe"]


class Compressed:
    extensions = [".zip", ".tar", ".rar", ".7z"]


class Applications:
    extensions = [".app"]


supported_files = [
    Music(),
    Projects(),
    Code(),
    Video(),
    Photos(),
    Documents(),
    Utilities(),
    Compressed(),
    Applications()
]


class App:
    def __init__(self):
        self.home_dir = Path.home()
        self.dirs = []
        self.files = []
        self.settings_file = f'{Path.home()}/Library/Application Support/Seiri/settings.json'
        self.read_settings()
        self.sort()
        self.catalogue_files()
        self.catalogue_dirs()
        self.end()

    def end(self):
        messagebox.showinfo(title="Seiri", message="All organized.")

    def sort(self):
        for _dir in os.listdir(self.start_dir):
            abs_path = os.path.join(self.start_dir, _dir)
            if os.path.isdir(abs_path): self.dirs.append(_dir)
            elif os.path.isfile(abs_path): self.files.append(_dir)

    def catalogue_files(self):
        for file in self.files:
            abs_path = os.path.join(self.start_dir, file)
            name, extension = os.path.splitext(abs_path)
            if name and extension:
                for supported in supported_files:
                    if extension.lower() in supported.extensions:
                        target = os.path.join(self.seiri_dir,
                                              type(supported).__name__)
                        if not os.path.exists(target): os.makedirs(target)
                        os.rename(abs_path, os.path.join(target, file))

    def catalogue_dirs(self):
        for _dir in self.dirs:
            abs_path = os.path.join(self.start_dir, _dir)
            files = os.listdir(os.path.join(self.start_dir, _dir))
            extensions = []
            dir_count = 0
            file_count = 0

            # Peek into child nodes
            for _file in files:
                _abs_path = os.path.join(self.start_dir, _dir, _file)
                name, extension = os.path.splitext(_abs_path)
                if os.path.isfile(_abs_path):
                    file_count += 1
                    if extension: extensions.append(extension)
                elif os.path.isdir(_abs_path):
                    dir_count += 1
                    if extension: extensions.append(extension)

            if len(extensions):
                most_common_extension, frequency = collections.Counter(
                    extensions).most_common()[0]

                for supported in supported_files:
                    if most_common_extension.lower() in supported.extensions:
                        target = os.path.join(self.seiri_dir,
                                              type(supported).__name__)
                        if not os.path.exists(target): os.makedirs(target)
                        os.rename(abs_path, os.path.join(target, _dir))
                        print('Moving was successful.')
            else:
                print('No criteria to organize: initiating os.walk')
                extensions = []
                for root, dirs, files in os.walk(self.start_dir, topdown=True):
                    for name in files:
                        file_name, file_extension = os.path.splitext(name)
                        if file_extension:
                            extensions.append(file_extension)
                    for dir_name in dirs:
                        file_name, file_extension = os.path.splitext(name)
                        if file_extension:
                            extensions.append(file_extension)

                if len(extensions):
                    most_common_extension, frequency = collections.Counter(
                        extensions).most_common()[0]
                    for supported in supported_files:
                        if most_common_extension.lower(
                        ) in supported.extensions:
                            target = os.path.join(self.seiri_dir,
                                                  type(supported).__name__)
                            if not os.path.exists(target): os.makedirs(target)
                            os.rename(abs_path, os.path.join(target, _dir))
                            print('Moving was successful.')

    def read_settings(self):
        if os.path.exists(self.settings_file):
            settings = json.loads(open(self.settings_file, 'r+').read())
            self.seiri_dir = settings["seiri_dir"]
        else:
            messagebox.showinfo(
                title=None,
                message=
                f'Welcome to Seiri.\n\nWhere do you want to organize files?')
            user_dir = filedialog.askdirectory(initialdir="/")
            self.seiri_dir = os.path.join(user_dir, 'Seiri')

            os.makedirs(f"{Path.home()}/Library/Application Support/Seiri")
            self.settings_file = f"{Path.home()}/Library/Application Support/Seiri"
            if not os.path.exists(self.settings_file):
                os.makedirs(self.settings_file)
            with open(f"{self.settings_file}/settings.json",
                      'w+') as json_file:
                new_settings = {"seiri_dir": self.seiri_dir}
                json.dump(new_settings, json_file)
        messagebox.showinfo(
            title=None,
            message=f'What folder would you like to put in the catalogue?')
        self.start_dir = filedialog.askdirectory(initialdir=Path.home())
        print(self.start_dir)


app = App()

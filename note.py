# -*- coding: utf-8 -*-

from colorama import init
from termcolor import colored, cprint
import os
import sys
import random
init()

FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))
DEFAULT_NOTE_FOLDER = os.path.join(FILE_LOCATION, 'notes')
DEFAULT_EDITOR = "code"





class Note():
    def __init__(self):
        self.commands = {
            'help': self.get_help,
            'c': self.create,
            'create': self.create,
            'o': self.open_file,
            'open': self.open_file,
            'list': self.list_notes
        }

        self.commands_help = {
            'help': 'Display all commands with their usage examples',
            'c': 'Shortcut for create',
            'create': 'Create file and open it with default editor; usage: $note create --dir="<dir>" <file.extension>',
            'o': 'Shortcut for open',
            'open': 'Open existing note with default editor; usage: $note open --dir="<dir>" <file.extension>'
        }

        self.error_list = {
            'no_param': 'No parameters were given',
            'alrd_exist': 'The file that you want to create already exist\nUse "open" or "o" to open it',
            'dnt_exist': 'That file doesnt exist'
        }

    def open_file(self,args):
        file_name = args[-1]
        file_path = os.path.join(DEFAULT_NOTE_FOLDER, file_name)

        for a in args:
            if '--dir' in a:
                folder = a.split('=')[-1].replace('"',"")
                folder = os.path.join(DEFAULT_NOTE_FOLDER, folder)
                file_path = os.path.join((folder+'/'),file_name)

        if os.path.exists(file_path):
            os.system(f'{DEFAULT_EDITOR} {file_path}')
        else:
            error('dnt_exist')

    

    def check_note_folder(self): return True if os.path.exists(
        DEFAULT_NOTE_FOLDER) else False

    def get_help(self,args):
        print('============')
        cprint('Noter command list', attrs=['bold','underline'])
        print('============\n')
        for c in self.commands.keys():
            print('• ',end='')
            cprint(c,'green',end='')
            for i in range(20-len(c)):
                print(' ',end='')
            print(self.commands_help[c]) 

    def error(self,err, help=False):
        cprint(self.error_list[err], 'red')
        if help:
            self.get_help()

    def list_notes(self,args):
        for root, dirs, files in os.walk(DEFAULT_NOTE_FOLDER):
            for file in files:
                    _, path = os.path.join(root, file).split(DEFAULT_NOTE_FOLDER)
                    print(path)

    def create(self,args):

        file_name = args[-1]
        file_path = os.path.join(DEFAULT_NOTE_FOLDER, file_name)
        for a in args:
            if '--dir' in a:
                folder = a.split('=')[-1].replace('"',"")
                folder = os.path.join(DEFAULT_NOTE_FOLDER, folder)
                if not os.path.exists(folder):
                    os.mkdir(folder)
                file_path = os.path.join((folder+'/'),file_name)

        print(file_path)
        if os.path.exists(file_path):
            self.error('alrd_exist')
        else:
            open(f'{file_path}', 'x').close()
            cprint(
                f'File {file_name} was succesfully created in {file_path} :)', 'green')
            os.system(f'{DEFAULT_EDITOR} {file_path}')

    def main(self, sys_args):
        try:
            _, command, *params = sys_args
        except Exception:
            self.error('no_param', help=True)
            sys.exit()

        if self.check_note_folder() != True:
            os.mkdir(DEFAULT_NOTE_FOLDER)
        os.chdir(DEFAULT_NOTE_FOLDER)
        self.commands[command](params)


if __name__ == "__main__":
    Noter = Note()
    Noter.main(sys.argv)

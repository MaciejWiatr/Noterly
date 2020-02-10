# -*- coding: utf-8 -*-
import os
import sys
from functools import lru_cache
from colorama import init
from termcolor import cprint
from tabulate import tabulate

init()

FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))
DEFAULT_NOTE_FOLDER = os.path.join(FILE_LOCATION, 'notes')
DEFAULT_EDITOR = "notepad"


@lru_cache
class Note():
    def __init__(self):
        """Main noter module."""
        self.commands = {
            'help': self.get_help,
            'create': self.create,
            'open': self.open_file,
            'list': self.list_notes
        }

        self.opts = {
            '--dir': None
        }

        self.aliases = {
            'c': 'create',
            'o': 'open',
            'l': 'list',
            'h': 'help'
        }

        self.commands_help = {
            'help': 'Display all commands with their usage examples',
            'create': 'Create file and open it with default editor; usage: $note create --dir="<dir>" <file.extension>',
            'open': 'Open existing note with default editor; usage: $note open --dir="<dir>" <file.extension>',
            'list': 'Display note list'
        }

        self.error_list = {
            'no_param': 'No parameters were given',
            'alrd_exist': 'The file that you want to create already exist\nUse "open" or "o" to open it',
            'dnt_exist': 'That file doesnt exist',
            "wrong_command": "Invalid command"
        }

    def open_file(self, args):
        file_name = args[-1]

        if self.opts['--dir']:
            file_name = f"{self.opts['--dir']}\\{file_name}"

        file_path = os.path.join(DEFAULT_NOTE_FOLDER, file_name)

        if os.path.exists(file_path):
            os.system(f'{DEFAULT_EDITOR} {file_path}')
        else:
            self.error('dnt_exist')

    @staticmethod
    def check_note_folder():
        return True if os.path.exists(
            DEFAULT_NOTE_FOLDER) else False

    def get_help(self, *args):
        commands = list(self.commands.keys())
        descriptions = [self.commands_help[c] for c in commands]
        aliases = []
        for c in commands:
            for alias, command in self.aliases.items():
                if command == c:
                    aliases.append(alias)
        cprint(tabulate({"Command": commands,
                         "Alias": aliases,
                         "Description": descriptions}, headers="keys",), 'green')

    def error(self, err, get_help=False):
        cprint(self.error_list[err], 'red')
        if get_help:
            self.get_help()
        sys.exit()

    @staticmethod
    def list_notes(args):
        for root, _, files in os.walk(DEFAULT_NOTE_FOLDER):
            for file in files:
                _, path = os.path.join(root, file).split(DEFAULT_NOTE_FOLDER)
                print(path)

    def create(self, args):

        file_name = args[-1]

        if self.opts['--dir']:
            folder = os.path.join(DEFAULT_NOTE_FOLDER, str(self.opts['--dir']))
            if not os.path.exists(folder):
                os.mkdir(folder)
            file_name = f"{self.opts['--dir']}\\{file_name}"

        file_path = os.path.join(DEFAULT_NOTE_FOLDER, file_name)
        if os.path.exists(file_path):
            self.error('alrd_exist', get_help=True)
        else:
            open(f'{file_path}', 'x').close()
        os.system(f'{DEFAULT_EDITOR} {file_path}')
        cprint(
            f'File {file_name} was succesfully created in {file_path} :)', 'green')

    def handle_aliases(self, command):
        if command in self.aliases.keys():
            return self.aliases[command]
        else:
            return command

    def parse_opts(self, sys_args):
        try:
            _, command, *params = sys_args
        except Exception:
            self.error('no_param', get_help=True)
            sys.exit()
        command = self.handle_aliases(command)
        if command not in self.commands.keys():
            self.error('wrong_command', get_help=True)

        for param in params:
            if "--" in param:
                opt, val = param.split("=")
                if opt in self.opts:
                    self.opts[opt] = val

        return [command, params]

    def main(self, sys_args):
        parsed = self.parse_opts(sys_args)
        command = parsed[0]
        params = parsed[1]
        if not self.check_note_folder():
            os.mkdir(DEFAULT_NOTE_FOLDER)
        os.chdir(DEFAULT_NOTE_FOLDER)
        self.commands[command](params)


if __name__ == "__main__":
    Noter = Note()
    Noter.main(sys.argv)

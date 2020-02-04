import json
import os


class JsonError(Exception):
    pass


def load_config():
    with open('config.json') as json_file:
        data = json.load(json_file)
    editor = data['default_editor']
    folder = data['default_folder']
    return [editor, folder]


def set_config(editor, folder):
    filename = 'config.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data['default_editor'] = editor
        data['default_folder'] = folder

    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

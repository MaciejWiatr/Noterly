import json
import os

CONFIG_FILE = 'config.json'


class JsonError(Exception):
    pass


def load_config():
    with open(CONFIG_FILE) as json_file:
        data = json.load(json_file)
    editor = data['default_editor']
    folder = data['default_folder']
    return [editor, folder]


def set_config(editor, folder):
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        data['default_editor'] = editor
        data['default_folder'] = folder

    os.remove(CONFIG_FILE)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

import os
import json
import contextlib


if 'HOME' in os.environ:
    HOME_KEY = 'HOME'
else:
    HOME_KEY = 'USERPROFILE'


@contextlib.contextmanager
def temp_home(new_home):
    default_home = os.environ[HOME_KEY]
    os.environ[HOME_KEY] = str(new_home)
    try:
        yield
    finally:
        os.environ[HOME_KEY] = default_home


def save_data(data, path, newline='\n'):
    with open(path, 'w', encoding='utf8', newline=newline) as f:
        json.dump(data, f, indent=0)

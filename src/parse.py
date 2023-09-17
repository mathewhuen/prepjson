import copy
import json
from pathlib import Path


from prepjson.constants import (
    KNOWN_HASHES,
    DATA_PATH,
    DIGITS,
    IGNORE,
)


class FILE:
    def __init__(self, file, start=0):
        # self.file = copy.deepcopy(file)
        self.file = file
        self.file.seek(start)
        self.index = start

    def get(self, suppress_whitespace=True):
        self.char = self.file.read(1)
        self.index += 1
        if suppress_whitespace and self.char in IGNORE:
            return self.get()
        return self.char


def is_special(char, reference, previous):
    if previous == "\\":
        return False
    return char == reference


def is_number(char, previous):
    return char in DIGITS+["-"]


def handle_string(f):
    r"""
    Return all characters from current location to next `"`.
    """
    output = list()
    while True:
        char = f.get(suppress_whitespace=False)
        if is_special(char, '"', ''):
            return ''.join(output)
        output.append(char)
        previous = char


def handle_number(f):
    r"""
    """
    output = [f.char]
    while True:
        char = f.get(suppress_whitespace=False)
        if char not in DIGITS + ["."]:
            n = ''.join(output)
            if '.' in n:
                return float(n), 'float'
            else:
                return  int(n), 'integer'
        output.append(char)


def handle_array(f):
    data = dict()
    key = 0
    char = f.get()
    while True:
        if is_special(char, '"', ''):
            start = f.index
            s = handle_string(f)
            data[(key,)] = {'start': start, 'end': f.index-1, 'type': 'string'}
            key += 1
        if is_special(char, "[", ''):
            start = f.index - 1
            array = handle_array(f)
            data[(key,)] = {'start': start, 'end': f.index, 'type': 'array'}
            for subkey, item in array.items():
                data[(key,)+subkey] = item
            key += 1
        if is_special(char, "{", ''):
            start = f.index - 1
            table = handle_table(f)
            data[(key,)] = {'start': start, 'end': f.index, 'type': 'table'}
            for subkey, item in table.items():
                data[(key,)+subkey] = item
            key += 1
        if is_number(char, ''):
            start = f.index - 1
            n, n_type = handle_number(f)
            data[(key,)] = {'start': start, 'end': f.index - 1, 'type': n_type}
            key += 1
            char = f.char
            continue  # skip getting new char
        if is_special(char, "]", ''):
            break
        char = f.get()
    return data

def handle_table(f):
    r"""
    Update json_data with table's key-value data.
    """
    previous = ''
    key = None
    data = dict()
    char = f.get()
    while True:
        if is_special(char, '"', previous):
            if key is None:
                key = handle_string(f)
            else:
                start = f.index
                value = handle_string(f)
                data[(key,)] = {'start': start, 'end': f.index-1, 'type': 'string'}
                key = None
        if is_number(char, previous):
            assert key is not None
            start = f.index - 1
            n, n_type = handle_number(f)
            data[(key,)] = {'start': start, 'end': f.index - 1, 'type': n_type}
            key = None
            char = f.char
            continue  # skip getting new char
        if is_special(char, "[", previous):
            assert key is not None
            start = f.index - 1
            array = handle_array(f)
            data[(key,)] = {'start': start, 'end': f.index, 'type': 'array'}
            for subkey, item in array.items():
                data[(key,)+subkey] = item
            key = None
        if is_special(char, "{", previous):
            assert key is not None
            start = f.index - 1
            table = handle_table(f)
            data[(key,)] = {'start': start, 'end': f.index, 'type': 'table'}
            for subkey, item in table.items():
                data[(key,)+subkey] = item
            key = None
        if is_special(char, "}", previous):
            break
        char = f.get()
    return data


def parse(path=None, open_kwargs=None, file=None, start=0):
    if path is not None:
        if open_kwargs is None:
            open_kwargs = dict()
        f = open(path, **open_kwargs)
    elif file is not None:
        f = file
    else:
        raise ValueError
    f = FILE(file=f, start=start)

    char = f.get()
    if is_special(char, "{", ''):
        data = handle_table(f)
    elif is_special(char, "[", ''):
        data = handle_array(f)
    else:
        message = (
            "parse was called on a file not formatted according to JSON "
            f"standards. The first character found was '{char}' but should "
            "be either '{' or '['."
        )
        raise RuntimeError(message)
    return data


if __name__ == '__main__':
    reference = parse('temp.json')
    print(reference)

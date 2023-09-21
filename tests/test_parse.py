import json
import pytest
from itertools import product


from prepjson.parse import (
    FILE,
    parse
)
from prepjson.load import load_from_reference


from data import DATA
from utils import save_data


@pytest.mark.parametrize(
    'labels,newline',
    product(
        DATA.values(),
        ['\n', '\r\n'],
    )
)
class TestParse:
    def test_reference(self, tmp_path, labels, newline):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path, newline=newline)
        json_reference = parse(data_path)
        if newline == '\n':
            label_key = 'reference'
        elif newline == '\r\n':
            label_key = 'reference_crlf'
        for key, value in json_reference.items():
            assert labels[label_key][key] == value

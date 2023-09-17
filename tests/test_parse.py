import json
import pytest


from prepjson.parse import (
    FILE,
    parse
)
from prepjson.load import load_from_reference


from data import DATA
from utils import save_data


@pytest.mark.parametrize(
    'labels',
    list(DATA.values()),
)
class TestParse:
    def test_reference(self, tmp_path, labels):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path)
        json_reference = parse(data_path)
        for key, value in json_reference.items():
            assert labels['reference'][key] == value

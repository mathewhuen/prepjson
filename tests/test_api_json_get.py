import json
import pytest
from pathlib import Path
from hashlib import sha256
from itertools import product


from prepjson import json_get, JSONLoader
from prepjson.load import preload


from data import DATA
from utils import save_data


class TestAPI:
    @pytest.mark.parametrize(
        'labels,do_preload',
        [
            [data, True] for data in DATA.values()
        ] + [
            [data, False] for data in DATA.values()
        ],
    )
    def test_json_get(self, tmp_path, labels, do_preload):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path)
        if do_preload:
            _ = preload(data_path)
        for key, value in labels['values'].items():
            loaded_value = json_get(data_path, key)
            assert loaded_value == value

    @pytest.mark.parametrize(
        'labels,do_preload,modify_mtime,modify_data',
        product(
            DATA.values(),  # data
            [True, False],  # do preload
            [True, False],  # modify mtime
            [True, False],  # modify data
        ),
    )
    def test_jsonloader(
            self,
            tmp_path,
            labels,
            do_preload,
            modify_mtime,
            modify_data,
    ):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path)
        if do_preload:
            _ = preload(data_path)
        loader = JSONLoader(data_path)
        if modify_mtime:
            save_data(labels['json'], data_path)
        if modify_data:
            with open(data_path, 'a') as f:
                f.seek(0, 2)  # go to end
                f.write(' ')
        for key, value in labels['values'].items():
            loaded_value = json_get(data_path, key)
            assert loaded_value == value

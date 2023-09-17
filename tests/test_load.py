import json
import pytest
from pathlib import Path
from hashlib import sha256


from prepjson.parse import (
    FILE,
    parse
)
from prepjson.load import (
    filehash,
    get_refpath,
    load_from_reference,
)
from prepjson.constants import DATA_PATH


from data import DATA
from utils import save_data


class TestLoad:
    @pytest.mark.parametrize(
        'labels',
        list(DATA.values()),
    )
    def test_load_from_reference(self, tmp_path, labels):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path)
        json_reference = parse(data_path)
        for key, reference in json_reference.items():
            data = load_from_reference(reference, data_path)
            assert labels['values'][key] == data

    @pytest.mark.parametrize(
        'labels',
        list(DATA.values()),
    )
    def test_filehash(self, tmp_path, labels):
        data_path = tmp_path / 'data.json'
        save_data(labels['json'], data_path)
        sha = sha256()
        with open(data_path, 'rb') as f:
            file_contents = f.read()
            sha.update(file_contents)
        assert filehash(data_path) == sha.hexdigest()

    #@pytest.mark.parametrize(
    #    'policy,filename',
    #    [
    #        ('singleref', DATA_PATH["single_ref_name"]),
    #        # ('multiref', DATA_PATH["multi_ref_name"]),
    #    ]
    #)
    #def test_get_refpath(self, policy, filename):
        # assert get_refpath('1234567', policy) == (Path(DATA_PATH["refdir"]) / '12' / '34' / '567' / filename)
    def test_get_refpath(self):
        assert get_refpath('1234567') == (Path(DATA_PATH["refdir"]) / '12' / '34' / '567.ref')

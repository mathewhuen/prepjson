import os
import pytest


from prepjson.constants import (
    set_refdir,
    reset_refdir,
)


from utils import temp_home


@pytest.fixture(autouse=True)
def set_temp_home(tmp_path_factory):
    path = tmp_path_factory.mktemp('temp')
    #os.environ["REFJSON_HOME"] = str(path)
    set_refdir(path)
    with temp_home(path):
        yield
    reset_refdir()
    return None

import os
from pathlib import Path


KNOWN_HASHES = dict()

_home = os.environ.get("REFJSON_HOME")
DATA_PATH = {
    "refdirname": ".refjson",
    "home": os.path.expanduser("~") if _home is None else _home,
    "refdir": None,
    "single_ref_name": ".single.ref",
    "multi_ref_name": ".multi.ref",
}


def get_refdir():
    if DATA_PATH.get("refdir") is not None:
        return DATA_PATH["refdir"]
    else:
        return Path(DATA_PATH["home"]) / DATA_PATH["refdirname"]


def set_refdir(path):
    path = Path(path)
    path.mkdir(exist_ok=True)
    DATA_PATH["refdir"] = path


def reset_refdir():
    DATA_PATH["refdir"] = None


IGNORE = [
    "\n",
    "\t",
    "\r",
    " ",
]
DIGITS = [str(i) for i in range(10)]

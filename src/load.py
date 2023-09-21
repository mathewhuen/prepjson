import copy
import json
import pickle
from pathlib import Path
from simple_file_checksum import get_checksum


from prepjson.constants import (
    KNOWN_HASHES,
    #DATA_PATH,
    DIGITS,
    IGNORE,
    get_refdir
)
from prepjson.parse import parse


def load_from_reference(reference, path):
    f = open(path, "rb")
    f.seek(reference["start"])
    string_data = f.read(reference["end"] - reference["start"])
    if reference["type"] == "string":
        return string_data.decode("utf-8")
    if reference["type"] == "table":
        return json.loads(string_data)
    if reference["type"] == "array":
        return json.loads(string_data)
    if reference["type"] == "float":
        return float(string_data)
    if reference["type"] == "integer":
        return int(string_data)
    raise RuntimeError


def filehash(path):
    return get_checksum(str(path), algorithm="SHA256").replace(' ', '')


#def get_refpath_(sha):
#    return DATA_PATH["refdir"] / sha[:2] / sha[2:4] / sha[4:]
#def get_refpath_singleref(sha):
#    return get_refpath_(sha) / DATA_PATH["single_ref_name"]
#def get_refpath_multiref(sha):
#    return get_refpath_(sha) / DATA_PATH["multi_ref_name"]
#def get_refpath(sha, policy='singleref'):
#    if policy == 'singleref':
#        return get_refpath_singleref(sha)
#    elif policy == 'multiref':
#        raise NotImplementedError('Only policy = "singleref" is supported.')
#        return get_refpath_multiref(sha)
#    else:
#        raise NotImplementedError
def get_refpath(sha):
    #return DATA_PATH["refdir"] / sha[:2] / sha[2:4] / (sha[4:] + '.ref')
    return get_refdir() / sha[:2] / sha[2:4] / (sha[4:] + '.ref')


def get_reference(sha=None, refpath=None):
    if refpath is None:
        assert sha is not None
        refpath = get_refpath(sha)
    with open(refpath, 'rb') as f:
        return pickle.load(f)


def file_match(path):
    if str(path) not in KNOWN_HASHES:
        return False
    file_mtime = path.stat().st_mtime
    if KNOWN_HASHES[str(path)]["mtime"] == file_mtime:
        return True
    file_sha = filehash(path)
    if KNOWN_HASHES[str(path)]["hash"] == file_sha:
        return True
    return False


def preload(
        path=None,
        open_kwargs=None,
):
    path = Path(path).resolve()
    # if known path, check hash and mtime. If match, use. else, parse again.
    if str(path) in KNOWN_HASHES:
        sha = KNOWN_HASHES[str(path)]["hash"]
        saved_mtime = KNOWN_HASHES[str(path)]["mtime"]
        file_mtime = path.stat().st_mtime
        if saved_mtime != file_mtime:
            file_sha = filehash(path)
            refpath = get_refpath(file_sha)
            if sha != file_sha and refpath.exists():
                # file changed but new file already hashed
                KNOWN_HASHES[str(path)] = {
                    "hash": file_sha,
                    "mtime": path.stat().st_mtime,
                    "refpath": refpath,
                }
            elif sha != file_sha:
                # file changed and new file not hashed
                ref = parse(
                    path=path,
                    open_kwargs=open_kwargs,
                )
                refpath.parent.mkdir(parents=True, exist_ok=True)
                #with open(refpath, 'w', encoding='utf8') as f:
                #    json.dump(ref, f)
                with open(refpath, 'wb') as f:
                    pickle.dump(ref, f)
                KNOWN_HASHES[str(path)] = {
                    "hash": file_sha,
                    "mtime": path.stat().st_mtime,
                    "refpath": refpath,
                }
            else:
                # mtime changed but file not modified
                KNOWN_HASHES[str(path)]["mtime"] = path.stat().st_mtime
        else:
            refpath = KNOWN_HASHES[str(path)]["refpath"]
        return get_reference(refpath=refpath)
    else:
        file_sha = filehash(path)
        refpath = get_refpath(file_sha)
        KNOWN_HASHES[str(path)] = {
            "hash": file_sha,
            "mtime": path.stat().st_mtime,
            "refpath": refpath,
        }
        if not refpath.exists():
            ref = parse(
                path=path,
                open_kwargs=open_kwargs,
            )
            refpath.parent.mkdir(parents=True, exist_ok=True)
            #with open(refpath, 'w', encoding='utf8') as f:
            #    json.dump(ref, f)
            with open(refpath, 'wb') as f:
                pickle.dump(ref, f)
        else:
            ref = get_reference(refpath=refpath)
        return ref


if __name__ == '__main__':
    reference = parse('temp.json')
    print(reference)
    keys = [
        ('a',), ('b',), ('cdef',), ('cdef','a'), ('cdef','b'), ('g',), ('g',0),
        ('g',1,'h'), ('g',2),
    ]
    for key in keys:
        print(f"{key}: {load_from_reference(reference[key], 'temp.json')}")

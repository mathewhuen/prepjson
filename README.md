# PrepJSON

A small library for preprocessing large json files for fast and low-memory
loading.

## Installation

```shell
pip install prepjson
```

## Quick Start


Data from JSON files can be accessed with one of two methods:
- json_get function
- JSONLoader class


```python
from prepjson import json_get, JSONLoader

path = 'path/to/file.json'
nested_keys = ('nested', 'keys', 0)

# json_get function
value = json_get(path, nested_keys)

# JSONLoader class
data = JSONLoader(path)
value = data.get(*keys)
```

Keys should be a tuple of string-based keys and integer-based array indices.
For example, based on the following JSON data,

```json
{
  "key1": {
    "key2": [
      {"key3": 1.0},
      {"key4": 3.1}
    ]
  }
}
```

key3's value from following JSON data can be accessed with the key tuple:
("key1", "key2", 0, "key3").

## Caveats

PrepJSON works by traversing a given JSON file and creating a reference file
that maps tuples of keys to byte locations in the JSON file. When retrieving a
specific value, PrepJSON uses the file's hash to look up its reference file then
loads only the needed bytes from the JSON file. Some points to remember:
- first-time loading: If a JSON file has not been preparsed, PrepJSON will do so
  the first time it attempts to load it.
  As such, data cannot be queried until this initial parsing is finished.
  Currently, this is not enforced in a thread-safe way, though this will be
  added in the future. To ensure that files are loaded before running your
  code, you may run
  ```python
  prepjson path/to/file.json
  ```
  to pre-parse your JSON file.
- modifying files: Avoid modifying files while using PrepJSON.
  When getting data from a parsed JSON file, PrepJSON first
  checks the file's mtime. If it has changed, PrepJSON will check the file's
  hash. If its hash has also changed, PrepJSON will re-parse the file before it
  can load any data. It is crucial that file
- Many-keyed JSON data: If your JSON file contains predominantly small-memory
  key-value pairs (e.g., {"0": 1, "1": 0, "2": 0, "3": 1, ...}), memory gains
  from using PrepJSON will be minimal or none since the reference file that
  PrepJSON creates may be just as large or larger than the target JSON file.
  Similarly, for nested JSON data with many short entries, PrepJSON will
  almost certainly be inefficient.

---

## TODO

- Benchmark current implementation.
  - If reference files are too big:
    - May need to save only low-level keys in the reference file and then
      rebuild high-level keys dynamically when fetching data to reduce the size
      of reference files.
    - May need to split reference files over several sub reference files.
- Add missing unit and integration tests.
- Add python dict-like API.
- Make thread- and process-safe.

---

## License

This work uses the MIT license (see LICENSE.md for the full text).

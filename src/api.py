from prepjson.load import (
    file_match,
    load_from_reference,
    preload,
)


def json_get(
        path,
        keys,
        **load_kwargs,
):
    ref = preload(
        path,
        **load_kwargs,
    )
    return load_from_reference(
        reference=ref[keys],
        path=path,
    )


class JSONLoader:
    def __init__(self, path):
        self.path = path
        self.ref = preload(
            self.path,
        )

    def get(self, *keys):
        if not file_match(self.path):
            self.ref = preload(
                self.path,
            )
        return load_from_reference(
            reference=self.ref[keys],
            path=self.path,
        )


def cli_parse():
    return None

DATA = {
    0: {
        'json': [
            {'0': ''},
            [1.0, 2.0],
            1.0,
            2,
            "asdf",
        ],
        'reference': {
            (0,): {'start': 2, 'end': 13, 'type': 'table'},
            (0, '0'): {'start': 10, 'end': 10, 'type': 'string'},
            (1,): {'start': 15, 'end': 27, 'type': 'array'},
            (1, 0): {'start': 17, 'end': 20, 'type': 'float'},
            (1, 1): {'start': 22, 'end': 25, 'type': 'float'},
            (2,): {'start': 29, 'end': 32, 'type': 'float'},
            (3,): {'start': 34, 'end': 35, 'type': 'integer'},
            (4,): {'start': 38, 'end': 42, 'type': 'string'},
        },
        'values': {
            (0,): {'0': ''},
            (0, '0'): '',
            (1,): [1.0, 2.0],
            (1, 0): 1.0,
            (1, 1): 2.0,
            (2,): 1.0,
            (3,): 2,
            (4,): "asdf",
        }
    },
    1: {
        'json': {
            '0': '',
            'a': 1,
            'b': [1.0, 2.0],
            'c': {'d': [1.2, -2.0], 'efg': [-4]},
            'hij': 'klmn',
        },
        'reference': {
            ('0',): {'start': 8, 'end': 8, 'type': 'string'},
            ('a',): {'start': 16, 'end': 17, 'type': 'integer'},
            ('b',): {'start': 24, 'end': 36, 'type': 'array'},
            ('b', 0): {'start': 26, 'end': 29, 'type': 'float'},
            ('b', 1): {'start': 31, 'end': 34, 'type': 'float'},
            ('c',): {'start': 43, 'end': 80, 'type': 'table'},
            ('c', 'd'): {'start': 50, 'end': 63, 'type': 'array'},
            ('c', 'd', 0): {'start': 52, 'end': 55, 'type': 'float'},
            ('c', 'd', 1): {'start': 57, 'end': 61, 'type': 'float'},
            ('c', 'efg'): {'start': 72, 'end': 78, 'type': 'array'},
            ('c', 'efg', 0): {'start': 74, 'end': 76, 'type': 'integer'},
            ('hij',): {'start': 90, 'end': 94, 'type': 'string'},
        },
        'values': {
            ('0',): '',
            ('a',): 1,
            ('b',): [1.0, 2.0],
            ('b', 0): 1.0,
            ('b', 1): 2.0,
            ('c',): {'d': [1.2, -2.0], 'efg': [-4]},
            ('c', 'd'): [1.2, -2.0],
            ('c', 'd', 0): 1.2,
            ('c', 'd', 1): -2.0,
            ('c', 'efg'): [-4],
            ('c', 'efg', 0): -4,
            ('hij',): 'klmn',
        }
    }
}

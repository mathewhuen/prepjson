import json
from pathlib import Path
from time import time as now


from data import get_data


from prepjson import json_get, JSONLoader


def mean(xs):
    return sum(xs) / len(xs)


def benchmark_run(
    max_elements,
    max_depth,
    value_size,
    reps=10,
):
    data = get_data(
        max_elements=max_elements,
        max_depth=max_depth,
        value_size=value_size,
    )
    path = Path('temp_data')
    path.mkdir(parents=True, exist_ok=True)
    path = path / '0.json'
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f)

    rj_times = list()
    js_times = list()
    loader = JSONLoader(path)
    for _ in range(reps):
        t0 = now()
        with open(path, 'rb') as f:
            data = json.load(f)
        for _ in range(max_depth):
            data = data[0]
        js_times.append(now() - t0)

        t0 = now()
        #json_get(path, keys=tuple([0]*max_depth))
        loader.get(*([0]*max_depth))
        rj_times.append(now() - t0)
    return {'rj': mean(rj_times), 'js': mean(js_times)}


def benchmark_grid():
    path = Path('results')
    path.mkdir(parents=True, exist_ok=True)
    path = path / 'results.json'
    output = dict()
    me_vals = [10_000, 100_000]
    md_vals = [1, 3]
    vs_vals = [1_000, 4_000]
    #me_vals = [10_000, 20_000, 30_000, 40_000, 60_000, 80_000, 100_000]
    #md_vals = [1, 2, 3]
    #vs_vals = [2, 5, 10, 20, 100, 500, 1_000]
    for me_i, me in enumerate(me_vals):
        print(f'{me_i+1} / {len(me_vals)}')
        for md in md_vals:
            for vs in vs_vals:
                results = benchmark_run(
                    max_elements=me,
                    max_depth=md,
                    value_size=vs,
                    reps=10,
                )
                output[f'{me}-{md}-{vs}'] = {
                    'meta': {'elements': me, 'depth': md, 'element_size': vs},
                    'bm': results,
                }
    with open(path, 'w', encoding='utf8') as f:
        json.dump(output, f, indent=2)


if __name__ == '__main__':
    benchmark_grid()

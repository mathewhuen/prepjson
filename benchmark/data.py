#import random


def add_elements(data, depth, max_elements, max_depth, value_size):
    count = 0
    for _ in range(max_elements // max_depth ** 2):
        if depth < max_depth:
            sub_data, n_new_items = add_elements(
                list(),
                depth + 1,
                max_elements,
                max_depth,
                value_size,
            )
            data.append(sub_data)
            count += n_new_items
        else:
            data.append('.'*value_size)
            count += 1
        if count > max_elements:
            break
    return data, count


def get_data(max_elements, max_depth, value_size):
    #if random.uniform(0, 1) < 0.5:
    #    output = dict()
    #    mode = 'table'
    #else:
    #    output = list()
    #    mode = 'array'
    index = 0
    data = list()
    while index < max_elements:
        sub_data, n_new_items = add_elements(
            list(),
            0,
            max_elements,
            max_depth,
            value_size,
        )
        data.append(sub_data)
        index += n_new_items
    return data

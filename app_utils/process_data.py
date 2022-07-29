from math import ceil
def extract_values_json(json_file, keys):
    return {key: json_file[key] for key in keys}

def chop_list(lst, max_range):
        n_groups = ceil(len(lst) / max_range)
        return [lst[i::n_groups] for i in range(n_groups)]
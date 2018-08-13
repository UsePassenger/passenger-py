import pandas as pd


def indexall(arr, k):
    return [i for i, el in enumerate(arr) if el == k]


def keys2idx(all_keys, key_pairs):
    """ Since multiple tables have the same key, use a key
        and its offset to get the correct column index.
    """
    ret = []
    for i, k in key_pairs:
        ret.append(indexall(all_keys, k)[i])
    return ret


def timetable_view(rows, key_pairs=None):
    if not key_pairs:
        key_pairs = [
            (0, 'trip_id'),
            (0, 'service_id'),
            (0, 'stop_id'),
            (1, 'stop_id'),
            (0, 'arrival_time'),
            (1, 'arrival_time'),

        ]
    df = pd.DataFrame(rows, columns=rows[0].keys())
    df_keys = keys2idx(df.keys(), key_pairs)
    view = df.ix[:,df_keys]
    return view

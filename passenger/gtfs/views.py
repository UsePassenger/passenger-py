import pandas as pd


def timetable_view(rows):
    df = pd.DataFrame(rows, columns=rows[0].keys())
    view = df.ix[:, df.keys()]
    return view

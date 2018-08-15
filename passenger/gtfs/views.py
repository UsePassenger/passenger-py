import pandas as pd


def timetable_view(rows):
    print(len(rows))
    if len(rows) == 0:
        raise Exception("Rows are empty.")
    df = pd.DataFrame(rows, columns=rows[0].keys())
    view = df.ix[:, df.keys()]
    return view

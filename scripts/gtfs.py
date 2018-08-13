import argparse
import datetime
import json
import os

from passenger.gtfs.file_reader import FileReader
import passenger.gtfs.database as database
import passenger.gtfs.views as views
import passenger.utils.date as date
import passenger.utils.fs as fs
from passenger.utils.timer import Timer

from tqdm import tqdm
import pandas as pd


def build(options):
    gtfs_path = options.gtfs_path
    server_path = options.server_path
    db_path = os.path.join(server_path, 'gtfs.db')

    fns = FileReader(gtfs_path).read()

    database.build_database(fns, db_path)
    db = database.Database(db_path)


def query(options):
    server_path = options.server_path
    db_path = os.path.join(server_path, 'gtfs.db')

    db = database.Database(db_path)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    service_ids = db.service_ids_include(options.daystamp, options.use_calendar, options.use_calendar_dates)
    rows = db.query_stop_times(options.start, options.end, service_ids=service_ids)
    rows = list(rows)

    print('Found {} rows.'.format(len(rows)))

    view = views.timetable_view(rows)
    print(view)


def speedtest(options):
    server_path = options.server_path
    db_path = os.path.join(server_path, 'gtfs.db')

    db = database.Database(db_path)

    dt = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
    timedelta = datetime.timedelta(1)

    queries = [
        ('1', '74', dt),
    ]

    n = 300

    with Timer() as t:
        for start, end, dt in tqdm(queries):
            for i in tqdm(range(n)):
                dt = dt + timedelta * i

                daystamp = date.daystamp(dt)

                service_ids = db.service_ids_include(daystamp, options.use_calendar, options.use_calendar_dates)
                rows = db.query_stop_times(options.start, options.end, service_ids=service_ids)
                rows = list(rows)

                assert len(rows) > 0

    interval = t.interval
    one = interval / n

    print('N={} {} (N=1 {})'.format(n, interval, one))


def init_boolean_flags(options):
    flags_to_add = {}

    for k, v in options.__dict__.items():
        if isinstance(v, bool):
            if k.startswith('no'):
                flags_to_add[k[2:]] = not v
            else:
                flags_to_add['no' + k] = not v

    for k, v in flags_to_add.items():
        setattr(options, k, v)


def stringify_flags(options):
    # Ignore negative boolean flags.
    flags = {k: v for k, v in options.__dict__.items() if not k.startswith('no')}
    return json.dumps(flags, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Mode Selection
    parser.add_argument('--mode', default='build', choices=('build', 'query', 'speedtest'))

    # File Paths
    parser.add_argument('--gtfs_path', default=os.path.expanduser('~/data/passenger/mnr/latest'), type=str)
    parser.add_argument('--server_path', default=os.path.expanduser('~/data/passenger-server/mnr'), type=str)

    # Query Parameters
    parser.add_argument('--start', default='1', type=str)
    parser.add_argument('--end', default='74', type=str)
    parser.add_argument('--daystamp', default=date.daystamp(datetime.datetime.now()), type=str)
    parser.add_argument('--nouse_calendar', action='store_true')
    parser.add_argument('--nouse_calendar_dates', action='store_true')

    options = parser.parse_args()

    init_boolean_flags(options)

    print(stringify_flags(options))

    if options.mode == 'build':
        build(options)
    elif options.mode == 'query':
        query(options)
    elif options.mode == 'speedtest':
        speedtest(options)

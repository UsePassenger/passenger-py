import argparse
import os

from passenger.gtfs.file_reader import FileReader
import passenger.gtfs.database as database
import passenger.utils.fs as fs


def build(options):
    gtfs_path = options.gtfs_path
    server_path = options.server_path
    db_path = os.path.join(server_path, 'gtfs.db')

    if os.path.exists(db_path):
        raise FileExistsError('The database file already exists. Please delete it if desired.')

    fns = FileReader(gtfs_path).read()

    database.build_database(fns, db_path)
    db = database.Database(db_path)


def query(options):
    # TODO
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='build', choices=('build', 'query'))
    parser.add_argument('--gtfs_path', default=os.path.expanduser('~/data/passenger/mnr/latest'), type=str)
    parser.add_argument('--server_path', default=os.path.expanduser('~/data/passenger-server/mnr'), type=str)
    options = parser.parse_args()

    if options.mode == 'build':
        build(options)
    elif options.mode == 'query':
        query(options)

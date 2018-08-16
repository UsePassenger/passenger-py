import argparse

from passenger.gtfs.database import get_url
from passenger.server.app import launch


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Network Parameters
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--host', type=str, default='0.0.0.0')

    # DB Parameters
    parser.add_argument('--username', default='passenger', type=str)
    parser.add_argument('--password', default='passenger', type=str)
    parser.add_argument('--dbhost', default='localhost', type=str)
    parser.add_argument('--dbname', default='passenger', type=str)

    options = parser.parse_args()

    url = get_url(
        username=options.username,
        password=options.password,
        host=options.dbhost,
        dbname=options.dbname)

    launch(
        host=options.host,
        port=options.port,
        url=url,
        )

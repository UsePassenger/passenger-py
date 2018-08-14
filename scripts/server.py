import argparse

from passenger.server.app import launch


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--host', type=str, default='0.0.0.0')
    options = parser.parse_args()

    launch(
        host=options.host,
        port=options.port,
        )

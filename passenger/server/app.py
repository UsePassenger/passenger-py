"""
A simple flask server that responds to queries.

"""

import datetime
import os

from flask import Flask
from flask import jsonify
from flask import request
from flask import session

from passenger.server.response import BaseResponse, QueryResponse, ResponseJSONEncoder
from passenger.utils.date import daystamp as convert_to_daystamp
import passenger.gtfs.database as database


app = Flask(__name__)
app.json_encoder = ResponseJSONEncoder


def object_mapper(o):
    return {'{:02}_{}'.format(i, k): v for i, (k, v) in enumerate(o.items())}


@app.route('/')
def home():
    response = BaseResponse(msg='Hello World!')
    return jsonify(response)


@app.route('/api')
def api_home():
    response = BaseResponse(msg='Hello API!')
    return jsonify(response)


@app.route('/api/query')
def query():
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    daystamp = request.args.get('daystamp', None)

    if daystamp is None:
        daystamp = convert_to_daystamp(datetime.datetime.now())

    use_calendar = app.config['use_calendar']
    use_calendar_dates = app.config['use_calendar_dates']
    server_path = app.config['server_path']
    dburl = app.config['dburl']
    db_path = os.path.join(server_path, 'gtfs.db')

    db = database.APIDB(db_path, use_calendar=use_calendar, use_calendar_dates=use_calendar_dates, url=dburl)
    rows = db.query(departure, destination, daystamp)

    response = QueryResponse(
        departure=departure,
        destination=destination,
        daystamp=daystamp,
        results=rows,
        )

    return jsonify(response)


def launch(server_path=os.path.expanduser('~/data/passenger-server/mnr'), host='0.0.0.0', port=5001, url=None):
    app.config['server_path'] = server_path
    app.config['use_calendar'] = True
    app.config['use_calendar_dates'] = True
    app.config['dburl'] = url

    app.run(debug=True, host=host, port=port)

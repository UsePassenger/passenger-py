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


@app.route('/')
def home():
    response = BaseResponse(msg='Hello World!')
    return jsonify(response)


@app.route('/query')
def query():
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    daystamp = request.args.get('daystamp', None)

    if daystamp is None:
        daystamp = convert_to_daystamp(datetime.datetime.now())

    use_calendar = app.config['use_calendar']
    use_calendar_dates = app.config['use_calendar_dates']
    server_path = app.config['server_path']
    db_path = os.path.join(server_path, 'gtfs.db')
    db = database.Database(db_path)

    service_ids = db.service_ids_include(daystamp, use_calendar, use_calendar_dates)
    rows = db.query_stop_times(departure, destination, service_ids=service_ids)

    response = QueryResponse(
        departure=departure,
        destination=destination,
        daystamp=daystamp,
        results=rows,
        )

    return jsonify(response)


# def query(options):
#     server_path = options.server_path
#     db_path = os.path.join(server_path, 'gtfs.db')

#     db = database.Database(db_path)

#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_rows', None)
#     service_ids = db.service_ids_include(options.daystamp, options.use_calendar, options.use_calendar_dates)
#     rows = db.query_stop_times(options.start, options.end, service_ids=service_ids)
#     rows = list(rows)

#     print('Found {} rows.'.format(len(rows)))

#     view = views.timetable_view(rows)
#     print(view)


def launch(server_path=os.path.expanduser('~/data/passenger-server/mnr')):
    app.config['server_path'] = server_path
    app.config['use_calendar'] = True
    app.config['use_calendar_dates'] = True

    app.run(debug=True)

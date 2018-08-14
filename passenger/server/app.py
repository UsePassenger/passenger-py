"""
A simple flask server that responds to queries.

"""

import datetime

from flask import Flask
from flask import jsonify
from flask import request

from passenger.server.response import BaseResponse, QueryResponse, ResponseJSONEncoder

from passenger.utils.date import daystamp as convert_to_daystamp


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

    results = []

    response = QueryResponse(
        departure=departure,
        destination=destination,
        daystamp=daystamp,
        results=results,
        )

    return jsonify(response)


def launch():
	app.run(debug=True)

import argparse
import random
import json
import os

import numpy as np

from passenger.simulate.osm import read_csv, OSMPoints
from passenger.simulate.track import TrackGenerator
from passenger.simulate.schedule import ScheduleGenerator


cdir = os.path.dirname(os.path.realpath(__file__))


def run(options):
	print(json.dumps(options.__dict__))

	random.seed(options.seed)
	np.random.seed(options.seed)

	# Read Data
	points = read_csv(options.input)

	# Sample Points
	osmp = OSMPoints(points,
		limit=options.limit,
		start=(options.startx, options.starty),
		end=(options.endx, options.endy),
		)

	osmp.write('example.png')

	# Generate Track
	tg = TrackGenerator(osmp,
		mindist=options.mindist,
		noise_scale=options.noise_scale,
		)

	path, pathindex = tg.generate()
	pathnames = [osmp.names[i] for i in pathindex]

	osmp.write('example-path.png', path=path)
	osmp.write('example-names.png', path=path, names=pathnames)

	# Generate Schedule
	sg = ScheduleGenerator(path, ntrains=2)
	schedule = sg.generate()

	for row in schedule:
		print(row[0], row[1], ScheduleGenerator.format_time(row[2]))


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('--seed', type=int, default=11)

	# OSM
	parser.add_argument('--input', type=str, default=os.path.join(cdir, '..', 'passenger/simulate/examples/map-nyc.csv'))
	parser.add_argument('--limit', type=int, default=1000)
	parser.add_argument('--startx', type=float, default=-73.95)
	parser.add_argument('--starty', type=float, default=40.7)
	parser.add_argument('--endx', type=float, default=-73.85)
	parser.add_argument('--endy', type=float, default=41.1)

	# Track Generator
	parser.add_argument('--mindist', type=float, default=0.02)
	parser.add_argument('--noise_scale', type=float, default=11)

	options = parser.parse_args()

	run(options)

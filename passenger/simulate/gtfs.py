from passenger.simulate.schedule import ScheduleParser


class GTFSGenerator(object):
	def __init__(self, schedule):
		super(GTFSGenerator, self).__init__()
		self.schedule = ScheduleParser(schedule)

	def generate_agency(self):
		"""
		agency.txt
		agency_id,agency_name,agency_url,agency_timezone,agency_phone,agency_lang
		"""
		pass

	def generate_stops(self):
		"""
		stops.txt
		stop_id,stop_name,stop_desc,stop_lat,stop_lon,stop_url,location_type,parent_station
		"""

		filename = 'stops.txt'
		header = 'stop_id,stop_name,stop_desc,stop_lat,stop_lon,stop_url,location_type,parent_station'
		stop_ids = self.schedule.stopids()

		print(filename)
		print(header)

		for stop_id in stop_ids:
			print('{stop_id},{stop_name},{stop_desc},{stop_lat},{stop_lon},{stop_url},{location_type},{parent_station}'.format(
				stop_id=stop_id,
				stop_name='-',
				stop_desc='-',
				stop_lat='-',
				stop_lon='-',
				stop_url='-',
				location_type='-',
				parent_station='-',
				))
		print()

	def generate_routes(self):
		"""
		routes.txt
		route_id,route_short_name,route_long_name,route_desc,route_type
		A,17,Mission,"The ""A"" route travels from lower Mission to Downtown.",3
		"""
		pass

	def generate_stop_times(self):
		"""
		stop_times.txt
		trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type
		"""
		pass

	def generate_calendar(self):
		"""
		calendar.txt
		service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date
		"""
		pass

	def generate_calendar_dates(self):
		"""
		calendar_dates.txt
		service_id,date,exception_type
		"""
		pass

	def generate_fare_attributes(self):
		"""
		fare_attributes.txt
		fare_id,price,currency_type,payment_method,transfers,transfer_duration
		"""
		pass

	def generate_fare_rules(self):
		"""
		fare_rules.txt
		fare_id,route_id,origin_id,destination_id,contains_id
		"""
		pass

	def generate_shapes(self):
		"""
		shapes.txt
		shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
		"""
		pass

	def generate_frequencies(self):
		"""
		frequencies.txt
		trip_id,start_time,end_time,headway_secs
		"""
		pass

	def generate_transfers(self):
		"""
		transfers.txt
		from_stop_id,to_stop_id,transfer_type,min_transfer_time
		"""
		pass

	def generate(self):
		self.generate_agency()
		self.generate_stops()
		self.generate_routes()

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passenger.gtfs import models
import pandas as pd
from tqdm import tqdm

from passenger.utils.date import is_dayname, is_daystamp, get_dayname
from passenger.utils.date import daystamp as convert_to_daystamp

tables = [
    ['agency', models.Agency],
    ['calendar', models.Calendar],
    ['calendar_dates', models.CalendarDates],
    # ['frequencies', models.Frequencies],
    ['routes', models.Routes],
    # ['shapes', models.Shapes],
    ['stop_times', models.StopTimes],
    ['stops', models.Stops],
    ['trips', models.Trips],
]

def all_strings(d):
    return dict([(k, str(v)) for k, v in d.items()])


def get_url():
    username = 'passenger'
    password = 'passenger'
    host = 'localhost'
    dbname = 'passenger'

    url = "mysql+pymysql://{username}:{password}@{host}/{dbname}".format(
      username=username,
      password=password,
      host=host,
      dbname=dbname)

    return url


def build_database(filenames, database_path):
    """
    # mysql instructions

    Initialize database:

      CREATE USER 'passenger'@'localhost' IDENTIFIED BY 'passenger';
      GRANT ALL PRIVILEGES ON *.* TO 'passenger'@'localhost';
      CREATE DATABASE passenger;
    """
    url = get_url()

    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    models.Base.metadata.create_all(engine)

    # For each Model/File
    for t, mdl in tables:
        if t in filenames:
            fn = filenames[t]

            headers = None
            delim = ','
            flush_every = 1000
            dirty = False

            # Read CSV
            with open(fn) as f:
                for i, line in tqdm(enumerate(f)):
                    line = line.strip()

                    # Read Headers
                    if i == 0:
                        headers = line.split(delim)
                        continue

                    # Parse Line
                    parts = line.split(delim)
                    row_dict = {k: v for k, v in zip(headers, parts)}
                    obj = mdl(**row_dict)

                    # Add to DB
                    session.add(obj)

                    dirty = True

                    # Flush every so often to minimize RAM usage.
                    if i > 0 and i % flush_every == 0:
                        session.flush()
                        session.commit()
                        dirty = False

            if dirty:
                session.flush()
                session.commit()
                dirty = False

    session.close()


class APIDB(object):
    """
    A more streamlined wrapper for the database
    that is convenient for the API.
    """
    def __init__(self, db_path, use_calendar=True, use_calendar_dates=True):
        self.db = Database(db_path)
        self.use_calendar = use_calendar
        self.use_calendar_dates = use_calendar_dates

    def format_date(self, daystamp, traintime):
      # TODO: Date parsing can become a bottleneck...
      # TODO: Do we need to double check the time zone?
      hr, m, s = traintime.split(':')

      hr = int(hr)
      if hr >= 24:
          hr = hr % 24
          delta = datetime.timedelta(1)
      else:
          delta = datetime.timedelta(0)

      dt = datetime.datetime.strptime('{} {:02}:{}:{}'.format(daystamp, hr, m, s), '%Y%m%d %H:%M:%S')
      dt += delta

      return dt.strftime('%b %d %H:%M:%S EDT %Y')

    def object_mapper(self, x, daystamp):
        return {
            "departure": {
                "date": self.format_date(daystamp, x.departure_time),
                "stationName": "Grand-Central",
                "stationId": 1,
                "routeId": 1,
                "directionId": 0
            },
            "destination": {
                "date": self.format_date(daystamp, x.destination_time),
                "stationName": "Scarsdale",
                "stationId": 2,
                "routeId": 1,
                "directionId": 0
            }
        }

    def query(self, departure, destination, daystamp=None):
        db = self.db
        use_calendar = self.use_calendar
        use_calendar_dates = self.use_calendar_dates

        if daystamp is None:
            daystamp = convert_to_daystamp(datetime.datetime.now())

        service_ids = db.service_ids_include(daystamp, use_calendar, use_calendar_dates)
        rows = db.query_stop_times(departure, destination, service_ids=service_ids)

        def om(x):
          return self.object_mapper(x, daystamp)

        rows = map(om, rows)

        return rows

class Database(object):
    def __init__(self, database_path):
        super(Database, self).__init__()
        self.database_path = database_path
        engine = create_engine(get_url())
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def calendar(self, dayname):

        assert is_dayname(dayname)

        query_tpl = """SELECT service_id
        FROM calendar
        WHERE {dayname} = "1"
        """

        query = query_tpl.format(
          dayname=dayname,
          )

        return query

    def calendar_dates(self, daystamp):

        assert is_daystamp(daystamp)

        query_tpl = """SELECT service_id, exception_type
        FROM calendar_dates
        WHERE "date" = '{daystamp}'
        """

        query = query_tpl.format(
          daystamp=daystamp,
          )

        return query

    def service_ids_calendar(self, dayname):
        query = self.calendar(dayname)
        return self.session.execute(query).fetchall()

    def service_ids_calendar_dates(self, daystamp):
        """ exception_types:
            - 1 - added
            - 2 - removed

            calendar_dates gets precedence over calendar
        """
        query = self.calendar_dates(daystamp)
        return self.session.execute(query).fetchall()

    def service_ids_include(self, daystamp, use_calendar, use_calendar_dates):
        if use_calendar:
            dayname = get_dayname(daystamp)
            calendar_rows = list(self.service_ids_calendar(dayname))
            calendar_included = set([row['service_id'] for row in calendar_rows])
        else:
            calendar_included = set()

        if use_calendar_dates:
            calendar_dates_rows = list(self.service_ids_calendar_dates(daystamp))

            _cdi = [row['service_id'] for row in calendar_dates_rows if row['exception_type'] is '1']
            _cdx = [row['service_id'] for row in calendar_dates_rows if row['exception_type'] is '2']

            calendar_dates_included = set(_cdi)
            calendar_dates_excluded = set(_cdx)
        else:
            calendar_dates_excluded, calendar_dates_included = set(), set()

        included = calendar_included.difference(calendar_dates_excluded
          ).union(calendar_dates_included)
        return included

    def query_stop_times(self, start="1", end="74", service_ids=[], filter_drop_off=True):
        query_tpl = """SELECT
          start_trips.trip_headsign as departure_station_name,
          start_stop_times.stop_id as departure_station_id,
          start_stop_times.departure_time as departure_time,
          start_trips.route_id as departure_route_id,
          start_trips.direction_id as departure_direction_id,
          end_trips.trip_headsign as destination_station_name,
          end_stop_times.stop_id as destination_station_id,
          end_stop_times.arrival_time as destination_time,
          end_trips.route_id as destination_route_id,
          end_trips.direction_id as destination_direction_id
        FROM
          trips as start_trips
        JOIN
          trips as end_trips on start_trips.trip_id = end_trips.trip_id
        JOIN
          stop_times as start_stop_times on start_stop_times.trip_id = start_trips.trip_id
        JOIN
          stop_times as end_stop_times on end_stop_times.trip_id = end_trips.trip_id
        WHERE
          start_stop_times.stop_id = "{start}"
        AND end_stop_times.stop_id = "{end}"
        AND start_stop_times.arrival_time < end_stop_times.arrival_time
        AND start_stop_times.trip_id = end_stop_times.trip_id
        {filter_drop_off_clause}
        {service_ids_clause}
        ORDER BY
          start_stop_times.arrival_time ASC,
          end_stop_times.arrival_time ASC
        """

        if filter_drop_off:
            filter_drop_off_clause = """
            AND start_stop_times.pickup_type = "0"
            AND end_stop_times.drop_off_type = "0"
            """
        else:
            filter_drop_off_clause = ""

        if len(service_ids) > 0:
            service_ids_str = "'{service_ids}'".format(
              service_ids="','".join(service_ids)
              )
            service_ids_clause = """
              AND start_trips.service_id in ({start_service_ids_str})
              AND end_trips.service_id in ({end_service_ids_str})
              """.format(
              start_service_ids_str=service_ids_str,
              end_service_ids_str=service_ids_str,
              )
        else:
            service_ids_clause = ""

        query = query_tpl.format(
          start=start,
          end=end,
          filter_drop_off_clause=filter_drop_off_clause,
          service_ids_clause=service_ids_clause,
          )

        return self.session.execute(query)

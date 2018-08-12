from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passenger.gtfs import models
import pandas as pd
from tqdm import tqdm

from passenger.utils.date import *

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

def build_database(filenames, database_path):
    """
    #Unix/Mac - 4 initial slashes in total
    engine = create_engine('sqlite:////absolute/path/to/foo.db')
    """
    engine = create_engine("sqlite:///{}".format(database_path), echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    models.Base.metadata.create_all(engine)

    for t, mdl in tables:
        if t in filenames:
            fn = filenames[t]
            df = pd.read_csv(fn)
            keys = df.keys()
            q = []
            for i, row in tqdm(df.iterrows()):
                q.append(mdl(**all_strings(row)))
            session.add_all(q)
            session.commit()
    session.close()

class Database(object):
    def __init__(self, database_path):
        super(Database, self).__init__()
        self.database_path = database_path

        engine = create_engine("sqlite:///{}".format(database_path), echo=True)
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
          start_trips.*,
          end_trips.*,
          start_stop_times.*,
          end_stop_times.*
        FROM
          trips as start_trips, trips as end_trips
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
            AND start_stop_times.pickup_type == "0"
            AND end_stop_times.drop_off_type == "0"
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

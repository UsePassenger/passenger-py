from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Agency(Base):
    __tablename__ = 'agency'
    
    agency_id = Column(String(256), primary_key=True)
    agency_name = Column(String(256)) 
    agency_url = Column(String(256))
    agency_timezone = Column(String(256))
    agency_phone = Column(String(256))
    agency_lang = Column(String(256))

class Calendar(Base):
    __tablename__ = 'calendar'
    
    service_id = Column(String(256), primary_key=True)
    monday = Column(String(256))
    tuesday = Column(String(256))
    wednesday = Column(String(256))
    thursday = Column(String(256))
    friday = Column(String(256))
    saturday = Column(String(256))
    sunday = Column(String(256))
    start_date = Column(String(256))
    end_date = Column(String(256))

class CalendarDates(Base):
    __tablename__ = 'calendar_dates'
    
    service_id = Column(String(256), primary_key=True)
    date = Column(String(256), primary_key=True)
    exception_type = Column(String(256), primary_key=True)

# class Frequencies(Base):
#     __tablename__ = 'frequencies'

#     id = Column(String(256), primary_key=True)

class Routes(Base):
    __tablename__ = 'routes'

    route_id = Column(String(256), primary_key=True)
    agency_id = Column(String(256))
    route_short_name = Column(String(256))
    route_long_name = Column(String(256))
    route_desc = Column(String(256))
    route_type = Column(String(256))
    route_url = Column(String(256))
    route_color = Column(String(256))
    route_text_color = Column(String(256))

class Shapes(Base):
    __tablename__ = 'shapes'

    shape_id = Column(String(256), primary_key=True)
    shape_pt_lat = Column(String(256))
    shape_pt_lon = Column(String(256))
    shape_pt_sequence = Column(String(256))
    shape_dist_traveled = Column(String(256))

class StopTimes(Base):
    __tablename__ = 'stop_times'

    trip_id = Column(String(256), primary_key=True)
    arrival_time = Column(String(256))
    departure_time = Column(String(256))
    stop_id = Column(String(256), primary_key=True)
    stop_sequence = Column(String(256))
    pickup_type = Column(String(256))
    drop_off_type = Column(String(256))

class Stops(Base):
    __tablename__ = 'stops'

    stop_id = Column(String(256), primary_key=True)
    stop_code = Column(String(256))
    stop_name = Column(String(256))
    stop_desc = Column(String(256))
    stop_lat = Column(String(256))
    stop_lon = Column(String(256))
    zone_id = Column(String(256))
    stop_url = Column(String(256))
    location_type = Column(String(256))
    parent_station = Column(String(256))
    wheelchair_accessible = Column(String(256))

class Trips(Base):
    __tablename__ = 'trips'
    
    route_id = Column(String(256))
    service_id = Column(String(256))
    trip_id = Column(String(256), primary_key=True)
    trip_headsign = Column(String(256))
    trip_short_name = Column(String(256))
    direction_id = Column(String(256))
    block_id = Column(String(256))
    shape_id = Column(String(256))
    wheelchair_boarding = Column(String(256))

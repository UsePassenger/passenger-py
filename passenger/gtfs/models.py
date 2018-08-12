from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Agency(Base):
    __tablename__ = 'agency'
    
    agency_id = Column(String, primary_key=True)
    agency_name = Column(String) 
    agency_url = Column(String)
    agency_timezone = Column(String)
    agency_phone = Column(String)
    agency_lang = Column(String)

class Calendar(Base):
    __tablename__ = 'calendar'
    
    service_id = Column(String, primary_key=True)
    monday = Column(String)
    tuesday = Column(String)
    wednesday = Column(String)
    thursday = Column(String)
    friday = Column(String)
    saturday = Column(String)
    sunday = Column(String)
    start_date = Column(String)
    end_date = Column(String)

class CalendarDates(Base):
    __tablename__ = 'calendar_dates'
    
    service_id = Column(String, primary_key=True)
    date = Column(String, primary_key=True)
    exception_type = Column(String, primary_key=True)

# class Frequencies(Base):
#     __tablename__ = 'frequencies'

#     id = Column(String, primary_key=True)

class Routes(Base):
    __tablename__ = 'routes'

    route_id = Column(String, primary_key=True)
    agency_id = Column(String)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(String)
    route_url = Column(String)
    route_color = Column(String)
    route_text_color = Column(String)

class Shapes(Base):
    __tablename__ = 'shapes'

    shape_id = Column(String, primary_key=True)
    shape_pt_lat = Column(String)
    shape_pt_lon = Column(String)
    shape_pt_sequence = Column(String)
    shape_dist_traveled = Column(String)

class StopTimes(Base):
    __tablename__ = 'stop_times'

    trip_id = Column(String, primary_key=True)
    arrival_time = Column(String)
    departure_time = Column(String)
    stop_id = Column(String, primary_key=True)
    stop_sequence = Column(String)
    pickup_type = Column(String)
    drop_off_type = Column(String)

class Stops(Base):
    __tablename__ = 'stops'

    stop_id = Column(String, primary_key=True)
    stop_code = Column(String)
    stop_name = Column(String)
    stop_desc = Column(String)
    stop_lat = Column(String)
    stop_lon = Column(String)
    zone_id = Column(String)
    stop_url = Column(String)
    location_type = Column(String)
    parent_station = Column(String)
    wheelchair_accessible = Column(String)

class Trips(Base):
    __tablename__ = 'trips'
    
    route_id = Column(String)
    service_id = Column(String)
    trip_id = Column(String, primary_key=True)
    trip_headsign = Column(String)
    trip_short_name = Column(String)
    direction_id = Column(String)
    block_id = Column(String)
    shape_id = Column(String)
    wheelchair_boarding = Column(String)

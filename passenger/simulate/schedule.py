"""

datetime reference

    dt = datetime.datetime(year=2018, month=2, day=3, hour=16, second=2)

    print(dt)

    print()

    print(dt + datetime.timedelta(1), 'day')
    print(dt + datetime.timedelta(0, 1), 'second')
    print(dt + datetime.timedelta(0, 0, 1), 'microsecond')
    print(dt + datetime.timedelta(0, 0, 0, 1), 'millisecond')
    print(dt + datetime.timedelta(0, 0, 0, 0, 1), 'minute')
    print(dt + datetime.timedelta(0, 0, 0, 0, 0, 1), 'hour')
    print(dt + datetime.timedelta(0, 0, 0, 0, 0, 0, 1), 'week')

    print()

    fmtstr = '%Y'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%m'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%d'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%H'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%M'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%S'; print(dt.strftime(fmtstr), '\t', fmtstr)

    print()

    fmtstr = '%I'; print(dt.strftime(fmtstr), '\t', fmtstr)
    fmtstr = '%p'; print(dt.strftime(fmtstr), '\t', fmtstr)

    >>>

    2018-02-03 16:00:02

    2018-02-04 16:00:02 day
    2018-02-03 16:00:03 second
    2018-02-03 16:00:02.000001 microsecond
    2018-02-03 16:00:02.001000 millisecond
    2018-02-03 16:01:02 minute
    2018-02-03 17:00:02 hour
    2018-02-10 16:00:02 week

    2018     %Y
    02   %m
    03   %d
    16   %H
    00   %M
    02   %S

    04   %I
    PM   %p

"""

import datetime

from passenger.simulate.distance import haversine


class ScheduleParser(object):
    def __init__(self, schedule):
        super(ScheduleParser, self).__init__()
        self.schedule = schedule

    def trainids(self):
        return set(x[0] for x in self.schedule)

    def stopids(self):
        return set(x[1] for x in self.schedule)
        

class ScheduleGenerator(object):
    """
    TODO: Need to account for acceleration and deceleration for a more accurate schedule.
    """

    average_speed = 10  # mph
    initial_date = datetime.datetime(year=2018, month=1, day=1, hour=7)
    one_hour = datetime.timedelta(0, 0, 0, 0, 0, 1)
    
    def __init__(self, path, ntrains, delay=datetime.timedelta(0, 0, 0, 0, 10)):
        self.path = path
        self.ntrains = ntrains
        self.delay = delay
        
    @staticmethod
    def format_time(dt):
        return dt.strftime('%Y%m%d#%I:%M%p')
        
    def simulate(self):
        start = self.initial_date
        path = self.path
        
        for trainid in range(self.ntrains):
            for stopid in range(0, path.shape[0]):
                if stopid == 0:
                    mytime = start + trainid * self.delay
                else:
                    pprev = path[stopid-1]
                    pnow = path[stopid]
                    dist = haversine(pprev[0], pprev[1], pnow[0], pnow[1])
        
                    mytime = mytime + dist / self.average_speed * self.one_hour

                yield (trainid, stopid, mytime)

    def generate(self):
        rows = []
        for row in self.simulate():
            rows.append(row)
        return rows

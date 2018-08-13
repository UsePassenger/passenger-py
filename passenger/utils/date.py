from datetime import datetime


def daystamp(dt):
    return dt.strftime('%Y%m%d')


def get_dayname(daystamp):
    d = datetime.strptime(daystamp, '%Y%m%d')
    day_idx = d.weekday()
    daynames = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
        ]
    result = daynames[day_idx]
    return result


def is_daystamp(daystamp):
    try:
        datetime.strptime(daystamp, '%Y%m%d')
    except:
        return False
    return True


def is_dayname(dayname):
    daynames = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
        ]
    return dayname in daynames

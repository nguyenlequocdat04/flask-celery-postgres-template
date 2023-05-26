import datetime as dt
import pytz


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return dt.datetime.now(pytz.utc)


def tzware_timestamp():
    return int(tzware_datetime().timestamp())


def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Amount of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = dt.date.today()

    delta = months * 365 / 12
    compare_date_with_delta = compare_date + dt.timedelta(delta)

    return compare_date_with_delta


def custom_tzware_datetime(year=None, month=None, day=None, hour=0, minute=0, second=0, microsecond=0):
    return dt.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=pytz.utc)


def to_tzware_dt(value: dt.datetime):
    return custom_tzware_datetime(
        value.year,
        value.month,
        value.day,
        value.hour,
        value.minute,
        value.second,
        value.microsecond,
    )

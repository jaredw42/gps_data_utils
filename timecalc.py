#!/usr/bin/env python3
import datetime
import sys

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LEAP_SECONDS = 18


def timecalc():
    """
    converts UTC datetimes to GPS weeks and seconds
    accepts UTC epoch time or UTC datetime in format  "%Y-%m-%d %H:%M:%S"
    """
    print("timecalc started. Ain't nobody got TIME for: \n")
    if len(sys.argv) == 2:
        print("single input argument, assuming this is a UTC epoch timestamp in ms")
        dt = int(sys.argv[1])
        dt = datetime.datetime.utcfromtimestamp(dt / 1000.0)
    else:
        if ":" in sys.argv[2]:
            dt = sys.argv[1] + " " + sys.argv[2]
            dt = datetime.datetime.strptime(dt, DATETIME_FORMAT)
        else:
            print("timecalc requires time in either UTC epoch time or datetime in {}".format(DATETIME_FORMAT))
            raise ValueError('UTC datetime needs to be {}'.format(DATETIME_FORMAT))

    gpstime = utctoweekseconds(dt)
    towsec = gpstime[2] + (gpstime[3] / 1000000.0)

    print("UTC DATETIME: {} \nGPS WEEK: {}, TOW: {}".format(dt, gpstime[0], towsec))


def utctoweekseconds(utc, leapseconds=18):

    """
    Returns the GPS week, day, seconds and microseconds since the beginning of the GPS week
    """
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00", datetimeformat)
    tdiff = utc - epoch + datetime.timedelta(seconds=leapseconds)
    gpsweek = tdiff.days // 7
    gpsdays = tdiff.days - 7 * gpsweek
    gpsseconds = tdiff.seconds + 86400 * (tdiff.days - 7 * gpsweek)

    return gpsweek, gpsdays, gpsseconds, tdiff.microseconds


if __name__ == "__main__":

    timecalc()

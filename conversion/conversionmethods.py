# -*- coding: utf-8 -*-
try:
    import ndb
except:
    # ndb not available in some environments when using Django
    pass
import json
import logging
import datetime
from dateutil import parser

#from google.appengine.ext import ndb

class BooleanNotRecognizedException(Exception): pass
class ShouldNotBeSearchedException(Exception):pass
class ShouldNotBeInRequesException(Exception):pass

booleanPositives = set(['true', 't', 'True', '1', True, 'T', 1, 'on', 'ON'])
booleanNegatives = set(['NoneType', 'None', None, 0, False, '', 'false', 'False', 'f', 'F', '0', '[]', '{}','()', 'off', 'OFF'])

dateFormat = '%Y-%m-%d'
dateSlashFormat = '%m/%d/%Y'
timeFormat = '%H:%M'
timeAMPMFormat = '%I:%M%p'

datetimeFormat = '%H:%M %Y-%m-%d'

def parseDateString(s):
    return parser.parse(s, ignoretz=True).date()

def parseTimeString(s):
    return parser.parse(s, ignoretz=True).time()

def parseDateTimeString(s):
    return parser.parse(s, ignoretz=True)

def raiseShouldNotBeInRequest(o):
    raise Exception, '- %s - Should not be in the request' % o

def stringToBool(s):
    if type(s) == bool: return s

    if not s:
        return False
    elif s in booleanPositives:
        return True
    elif s in booleanNegatives:
        return False
    else:
        raise BooleanNotRecognizedException, "Cannot tell if %s is true or false" % s

def stringToKey(s):
    return s
    return ndb.Key(urlsafe=s)

def stringToDate(s):
    format = dateSlashFormat if '/' in s else dateFormat
    return datetime.datetime.date(datetime.datetime.strptime(s, format))

def stringToTime(s):
    format = timeAMPMFormat if 'm' in s or 'M' in s else timeFormat
    return datetime.datetime.time(datetime.datetime.strptime(s, format))

def stringToDatetime(s):
    dformat = dateSlashFormat if '/' in s else dateFormat
    tformat = timeAMPMFormat if 'm' in s or 'M' in s else timeFormat
    return datetime.datetime.time(datetime.datetime.strptime(s, ' '.join([tformat, dformat])))

def returnSame(i):
    return i

def shouldNotBeSearched(_):
    raise ShouldNotBeSearchedException

def returnNothing(_):
    return ''

def returnSame(i):
    return i

def convertTimeToFloat(t):
    """ takes a time object, returns an float in military time"""
    return float(t.hour) + (float(t.minute)/60.0)

def convertToString(j):
    return unicode(j)

def convertStringToJSON(s):
    return json.loads(s)

def intToDatetime(f):
    return datetime.datetime.fromtimestamp(f)

def datetimeToInt(d):
    return d.strftime('%s')

def convertBoolToInt(s):
    isTrue = 1
    if s in booleanNegatives:
        isTrue = 0
    return isTrue

def convertIntToBool(s):
    if int(s) == 0:
        return False
    return True

def stringToNullBool(s):
    if type(s) == bool: return s
    if s == None or len(s) == 0:
        return None
    return stringToBool(s)

def keyToUrlsafe(o):
    return o.urlsafe()

def geoPtToDict(g):
    return {'latitude':g.lat, 'longitude':g.lon}


def formatDateForSearch(d):
    """ takes a datetime/date object and returns it formatted for search"""
    return "%d-%d-%d" % (d.year, d.month, d.day)

def convertFk(v):
    """ If a foreign key is nested, dig it out and return that"""
    if type(v) == dict:
        return v.get('id', '') or v.get('pk', '')
    return v

def toISO(obj):
    return obj.isoformat()

def fromISODate(s):
    return parser.parse(s).date()

def fromISOTime(s):
    return parser.parse(s).time()

def fractionToTime(f):  #TODO: move this into javascript to save on computing
    """ convert a fraction into its nearest 5 minute interval, returns datetime.time object"""
    if f > 24:
        return datetime.datetime.strptime('12:00', timeFormat)
    a = ((f % 1) * 60)
    hour = int(f)
    minute = (int(a / 5) * 5)
    return datetime.datetime.strptime("%d:%d" % (hour, minute), timeFormat)

def fractionToTimeString(f):
    """ turns a fraction into its nearest 5 minutes and outputs HH:MM"""
    return fractionToTime(f).strftime(timeFormat)

def convertFloatToTime(f):
    """ duplicate of fraction to time.  probably not used because it relies on time import"""
    if f > 23:
        return '12:00'
    a = ((f % 1) * 60)
    hour = int(f)
    minute = (int(a / 5) * 5)
    z = datetime.datetime.strptime("%d:%d" % (hour, minute), timeFormat)
    return time.mktime(z.timetuple())

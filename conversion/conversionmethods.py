# -*- coding: utf-8 -*-
import json
import logging
import datetime

#from google.appengine.ext import ndb

class BooleanNotRecognizedException(Exception): pass

booleanPositives = set(['true', 't', 'True', '1', True, 'T', 1, 'on', 'ON'])
booleanNegatives = set(['NoneType', 'None', None, 0, False, '', 'false', 'False', 'f', 'F', '0', '[]', '{}','()', 'off', 'OFF'])

dateFormat = '%Y-%m-%d'
dateSlashFormat = '%m/%d/%Y'
timeFormat = '%H:%M'
timeAMPMFormat = '%I:%M%p'

datetimeFormat = '%H:%M %Y-%m-%d'

def stringToBool(s):
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
    # commented out for django compatibility
    #return ndb.Key(urlsafe=s)

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

def keyToUrlsafe(o):
    return o.urlsafe()

def jsonToObj(j):
    return json.loads(j)

def geoPtToDict(g):
    return {'latitude':g.lat, 'longitude':g.lon}

def timeToJSONString(t):
    return t.strftime(timeFormat)

def dateToJSONString(d):
    return d.strftime(dateFormat)

def datetimeToJSONString(d):
    return d.strftime(datetimeFormat)

def formatDateForSearch(d):
    """ takes a datetime/date object and returns it formatted for search"""
    return "%d-%d-%d" % (d.year, d.month, d.day)


def categoriesToStrings(s):
    """ if the request sends categories like '1,4,5', this fixes them into strings"""
    return ','.join([CATEGORIES[int(i)] for i in s.split(',')])


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

#TODO: figure out whch of these methods is used, remove duplicates
def convertFloatToTime(f):
    """ duplicate of fraction to time.  probably not used because it relies on time import"""
    if f > 23:
        return '12:00'
    a = ((f % 1) * 60)
    hour = int(f)
    minute = (int(a / 5) * 5)
    z = datetime.datetime.strptime("%d:%d" % (hour, minute), timeFormat)
    return time.mktime(z.timetuple())

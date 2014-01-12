# -*- coding: utf-8 -*-
import json
import sys
import os
import decimal

from django.utils.safestring import SafeUnicode

from conversionmethods import convertTimeToFloat




try:
    from google.appengine.ext import ndb
except ImportError:
    from sweatguru import app_engine_paths
    sys.path.extend(app_engine_paths.getTestingPaths())

from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import blobstore

from conversionmethods import *

class TypeNotHandledException(Exception):pass
class ShouldNotBeSearchedException(Exception):pass
class ShouldNotBeInRequesException(Exception):pass

def raiseShouldNotBeInRequest(o):
    raise ShouldNotBeInRequesException, o


def convertValToJSON(v, permissive=False):
    """ in conversion from an object into JSON, we use these methods"""
    if not v:
        return ''
    elif v.__class__ in defaultPropertyMappings:
        return defaultPropertyMappings[v.__class__]['toJSON'](v) 

    else:
        if permissive:
            return v
        else:
            message = 'No type found for %s, class %s' % (v, v.__class__)
            raise TypeNotHandledException, message


class ComplexEncoder(json.JSONEncoder):
    def default(self, v):
        if v.__class__ in defaultPropertyMappings:
            return defaultPropertyMappings[v.__class__]['toJSON'](v) if defaultPropertyMappings[v.__class__]['toJSON'] else v

        else:
            if hasattr(v, 'urlsafe'):
                return v.urlsafe()
            elif hasattr(v, 'key'):
                x = dict([(p, getattr(v, p)) for p in v._properties])
                x.update({'urlsafe': v.key.urlsafe()})
                return x
            return json.JSONEncoder.default(self, v)

def valueFromRequest(kind, value):
    if kind in defaultPropertyMappings:
        return defaultPropertyMappings[kind]['fromRequest'](value)
    elif kind.__class__ in defaultPropertyMappings:
        return defaultPropertyMappings[kind.__class__]['fromRequest'](value)
    else:
        raise TypeNotHandledException, 'Type "%s" not handled for value "%s"' % (kind, value)

def toISO(obj):
    return obj.isoformat()


defaultPropertyMappings = {
        ndb.TextProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
        ndb.IntegerProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.NumberField, 'fromRequest': int, 'toJSON':returnSame},
        ndb.FloatProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.NumberField, 'fromRequest': float, 'toJSON': returnSame},
        ndb.BooleanProperty: {'toSearch': convertBoolToInt , 'toDatastore': convertIntToBool,'searchClass': search.NumberField, 'fromRequest': stringToBool, 'toJSON': returnSame},
        ndb.StringProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
        ndb.BlobProperty: {'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnNothing},
        ndb.DateTimeProperty: {'toSearch': datetimeToInt , 'toDatastore': intToDatetime,'searchClass': search.NumberField, 'fromRequest': stringToDatetime, 'toJSON':toISO},
        ndb.DateProperty: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.DateField, 'fromRequest': stringToDate, 'toJSON': toISO},
        ndb.TimeProperty: {'toSearch': convertTimeToFloat , 'toDatastore': convertFloatToTime,'searchClass': search.NumberField, 'fromRequest': stringToTime, 'toJSON':toISO},
        ndb.GeoPtProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.GeoField, 'fromRequest': returnSame, 'toJSON':geoPtToDict},
    
        ndb.GeoPt: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.GeoField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON':geoPtToDict},

        ndb.KeyProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': stringToKey, 'toJSON':keyToUrlsafe},
    
        blobstore.BlobKey:{'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON':returnNothing},
    
        blobstore.BlobInfo:{'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON':returnNothing},
        ndb.BlobKeyProperty: {'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON':returnNothing},
        ndb.UserProperty: {'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': stringToKey, 'toJSON':returnNothing},
        ndb.StructuredProperty: {'toSearch': returnSame , 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnSame},
        ndb.LocalStructuredProperty: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnSame},
        ndb.JsonProperty: {'toSearch': convertToString , 'toDatastore': convertStringToJSON,'searchClass': search.TextField, 'fromRequest': json.loads, 'toJSON':jsonToObj},
        ndb.PickleProperty: {'toSearch': shouldNotBeSearched , 'toDatastore': shouldNotBeSearched,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnSame},
        ndb.GenericProperty: {'toSearch': convertToString , 'toDatastore': convertToString,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
        ndb.ComputedProperty: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnSame},
        ndb.Key: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': stringToKey, 'toJSON':keyToUrlsafe},
        bool: {'toSearch': convertBoolToInt, 'toDatastore': convertIntToBool,'searchClass': search.NumberField, 'fromRequest': stringToBool, 'toJSON': returnSame},
        basestring: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},

        SafeUnicode: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},

        unicode: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
    
        str: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
    
        int: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass':  search.NumberField, 'fromRequest': int, 'toJSON': returnSame},

        long: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass':  search.NumberField, 'fromRequest': int, 'toJSON': int},

        float: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.NumberField, 'fromRequest': float, 'toJSON': returnSame},

        decimal.Decimal: {'toSearch': float, 'toDatastore': returnSame,'searchClass': search.NumberField, 'fromRequest': float, 'toJSON': float},
        dict: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': raiseShouldNotBeInRequest, 'toJSON': returnSame},
        list: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.TextField, 'fromRequest': returnSame, 'toJSON': returnSame},
        datetime.time: {'toSearch': convertTimeToFloat , 'toDatastore': convertFloatToTime,'searchClass': search.NumberField, 'fromRequest': stringToTime, 'toJSON':toISO},
        datetime.date: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.DateField, 'fromRequest': stringToDate, 'toJSON':toISO},
        datetime.datetime: {'toSearch': returnSame, 'toDatastore': returnSame,'searchClass': search.DateField, 'fromRequest': stringToDatetime, 'toJSON':toISO},


}

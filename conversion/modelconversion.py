# -*- coding: utf-8 -*-
import os
import sys
import json
import decimal

from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import blobstore

from conversionmap import conversionmap as cm

#try:
#    from google.appengine.ext import ndb
#except ImportError:
#    from sweatguru import app_engine_paths
#    sys.path.extend(app_engine_paths.getTestingPaths())



class TypeNotHandledException(Exception):pass
class ShouldNotBeSearchedException(Exception):pass
class ShouldNotBeInRequesException(Exception):pass


class DataEncoder(json.JSONEncoder):
    """ JSON Encoder that takes all of the property conversions into mind when converting data"""
    def default(self, v):
        if v.__class__ in cm:
            return cm[v.__class__]['toJSON'](v) if cm[v.__class__]['toJSON'] else v
        else:
            if hasattr(v, 'urlsafe'):
                return v.urlsafe()
            elif hasattr(v, 'key'):
                x = dict([(p, getattr(v, p)) for p in v._properties])
                x.update({'urlsafe': v.key.urlsafe()})
                return x
            return json.JSONEncoder.default(self, v)

def valueFromRequest(cls, value):
    """ Convert a value from a request into the kind the database expects"""
    if cls in cm:
        return cm[cls]['fromRequest'](value)
    elif cls.__class__ in cm:
        return cm[cls.__class__]['fromRequest'](value)
    else:
        raise TypeNotHandledException, 'Type "%s" not handled for value "%s"' % (cls, value)



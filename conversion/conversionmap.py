import decimal
from django.db import models
from jsonfield.fields import JSONField
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import blobstore
from conversionmethods import *
from django.utils.safestring import SafeUnicode


conversionmap = {
### NDB Types
    ndb.TextProperty: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },
    ndb.IntegerProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.NumberField,
        'fromRequest': int,
        'toJSON':returnSame
    },
    ndb.FloatProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.NumberField,
        'fromRequest': float,
        'toJSON': returnSame
    },
    ndb.BooleanProperty: {
        'toSearch': convertBoolToInt,
        'fromSearch': convertIntToBool,
        'searchClass': search.NumberField,
        'fromRequest': stringToBool,
        'toJSON': returnSame
    },
    ndb.StringProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },
    ndb.BlobProperty: {
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON': returnNothing
    },
    ndb.DateTimeProperty: {
        'toSearch': datetimeToInt ,
        'fromSearch': intToDatetime,
        'searchClass': search.NumberField,
        'fromRequest': parseDateTimeString,
        'toJSON':toISO
    },
    ndb.DateProperty: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.DateField,
        'fromRequest': parseDateString,
        'toJSON': toISO
        },
    ndb.TimeProperty: {
        'toSearch': convertTimeToFloat ,
        'fromSearch': convertFloatToTime,
        'searchClass': search.NumberField,
        'fromRequest': parseTimeString,
        'toJSON':toISO
    },
    ndb.GeoPtProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.GeoField,
        'fromRequest': returnSame,
        'toJSON':geoPtToDict
    },
    ndb.GeoPt: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.GeoField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON':geoPtToDict
    },
    ndb.KeyProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': stringToKey,
        'toJSON':keyToUrlsafe
    },
    blobstore.BlobKey:{
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON':returnNothing
    },

    blobstore.BlobInfo:{
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON':returnNothing
    },
    ndb.BlobKeyProperty: {
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON':returnNothing
    },
    ndb.UserProperty: {
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': stringToKey,
        'toJSON':returnNothing
    },
    ndb.StructuredProperty: {
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON': returnSame
    },
    ndb.LocalStructuredProperty: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON': returnSame
    },
    ndb.JsonProperty: {
        'toSearch': convertToString ,
        'fromSearch': convertStringToJSON,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': json.loads,
    },
    ndb.PickleProperty: {
        'toSearch': shouldNotBeSearched ,
        'fromSearch': shouldNotBeSearched,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON': returnSame
    },
    ndb.GenericProperty: {
        'toSearch': convertToString ,
        'fromSearch': convertToString,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON':
        returnSame
    },
    ndb.ComputedProperty: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': raiseShouldNotBeInRequest,
        'toJSON': returnSame
    },
    ndb.Key: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': stringToKey,
        'toJSON':keyToUrlsafe
    },


### Generic types

    bool: {
        'toSearch': convertBoolToInt,
        'fromSearch': convertIntToBool,
        'searchClass': search.NumberField,
        'fromRequest': stringToBool,
        'toJSON': returnSame
    },
    basestring: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },
    SafeUnicode: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },

    unicode: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },

    str: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },

    int: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass':  search.NumberField,
        'fromRequest': int,
        'toJSON': returnSame
    },
    long: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass':  search.NumberField,
        'fromRequest': int,
        'toJSON': int
    },
    float: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.NumberField,
        'fromRequest': float,
        'toJSON': returnSame
    },

    decimal.Decimal: {
        'toSearch': float,
        'fromSearch': returnSame,
        'searchClass': search.NumberField,
        'fromRequest': float,
        'toJSON': float
    },
    dict: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': convertFk,  ## want to take a dictionary and get foreign key because it is nested
        'toJSON': returnSame
    },
    list: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },
    datetime.time: {
        'toSearch': convertTimeToFloat ,
        'fromSearch': convertFloatToTime,
        'searchClass': search.NumberField,
        'fromRequest': fromISOTime,
        'toJSON':toISO
    },
    datetime.date: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.DateField,
        'fromRequest': parseDateString,
        'toJSON':toISO
    },
    datetime.datetime: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.DateField,
        'fromRequest': parseDateTimeString,
        'toJSON':toISO,
    },

### Django Specific models

    models.AutoField: { # Like integer field
        'toSearch': returnSame ,
        'fromSearch': returnSame,
        'searchClass': search.NumberField,
        'fromRequest': int,
        'toJSON': returnSame,
    },

    models.DateField: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.DateField,
        'fromRequest': fromISODate,
        'toJSON':toISO
    },

    models.TimeField: {
        'toSearch': convertTimeToFloat ,
        'fromSearch': convertFloatToTime,
        'searchClass': search.NumberField,
        'fromRequest': parseTimeString,
        'toJSON':toISO,
    },

    models.IntegerField: {
        'toSearch': int,
        'fromSearch': int,
        'searchClass': search.NumberField,
        'fromRequest': int,
        'toJSON': returnSame,
    },
    models.DateTimeField: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.DateField,
        'fromRequest': parseDateTimeString,
        'toJSON':toISO
    },
    models.FloatField: {
        'toSearch': float,
        'fromSearch': float,
        'searchClass': search.NumberField,
        'fromRequest': float,
        'toJSON': returnSame,
    },

    models.BooleanField: {
        'toSearch': convertBoolToInt,
        'fromSearch': convertIntToBool,
        'searchClass': search.NumberField,
        'fromRequest': stringToBool,
        'toJSON': returnSame
    },

    models.NullBooleanField: {
        'toSearch': convertBoolToInt,
        'fromSearch': convertIntToBool,
        'searchClass': search.NumberField,
        'fromRequest': stringToNullBool,
        'toJSON': returnSame
    },
    
    models.CharField: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },

    models.URLField: {
        'toSearch': returnSame,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': returnSame
    },

    JSONField: {
        'toSearch': convertToString ,
        'fromSearch': convertStringToJSON,
        'searchClass': search.TextField,
        'fromRequest': returnSame,
        'toJSON': json.loads,
    },

    models.OneToOneField: {
        'toSearch': convertToString ,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': convertFk,
        'toJSON': returnSame,
    },

    models.ForeignKey: {
        'toSearch': convertToString ,
        'fromSearch': returnSame,
        'searchClass': search.TextField,
        'fromRequest': convertFk,
        'toJSON': returnSame,
    },

## Not yet cared about
    
#    models.BigIntegerField
#    models.BinaryField
#    models.CommaSeparatedIntegerField
#    models.EmailField
#    models.FileField
#    models.FilePathField
#    models.ImageField
#    models.IPAddressField
#    models.GenericIPAddressField
#    models.PositiveIntegerField
#    models.PositiveSmallIntegerField
#    models.SlugField
#    models.SmallintegerField
#    models.TextField



}

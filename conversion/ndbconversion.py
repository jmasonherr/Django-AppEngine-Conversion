
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import blobstore
import conversionmethods.



ndb_types = {
        ndb.TextProperty: {
            'toSearch': conversionmethods.returnSame ,
            'toDatastore': returnSame,
            'searchClass': search.TextField,
            'fromRequest': returnSame,
            'toJSON': returnSame
        },
        ndb.IntegerProperty: {
            'toSearch': returnSame ,
            'toDatastore': returnSame,
            'searchClass': search.NumberField, 'fromRequest': int, 'toJSON':returnSame},
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


}



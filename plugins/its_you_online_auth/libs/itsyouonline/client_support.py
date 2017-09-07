"""
support methods for python clients
"""

import json
import collections
from datetime import datetime
from uuid import UUID
from enum import Enum
from dateutil import parser

# python2/3 compatible basestring, for use in to_dict
try:
    basestring
except NameError:
    basestring = str


def timestamp_from_datetime(datetime):
    """
        Convert from datetime format to timestamp format
        Input: Time in datetime format
        Output: Time in timestamp format
    """
    return datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def timestamp_to_datetime(timestamp):
    """
        Convert from timestamp format to datetime format
        Input: Time in timestamp format
        Output: Time in datetime format
    """
    return parser.parse(timestamp).replace(tzinfo=None)


def has_properties(cls, property, child_properties):
    for child_prop in child_properties:
        if getattr(property, child_prop, None) is None:
            return False

    return True


def list_factory(val, member_type):
    if not isinstance(val, list):
        raise ValueError('list_factory: value must be a list')
    return [val_factory(v, member_type) for v in val]


def dict_factory(val, objmap):
    # objmap is a dict outlining the structure of this value
    # its format is {'attrname': {'datatype': [type], 'required': bool}}
    objdict = {}
    for attrname, attrdict in objmap.items():
        value = val.get(attrname)
        if value is not None:
            for dt in attrdict['datatype']:
                try:
                    if isinstance(dt, dict):
                        objdict[attrname] = dict_factory(value, attrdict)
                    else:
                        objdict[attrname] = val_factory(value, [dt])
                except Exception:
                    pass
            if objdict.get(attrname) is None:
                raise ValueError(
                    'dict_factory: {attr}: unable to instantiate with any supplied type'.format(attr=attrname))
        elif attrdict.get('required'):
            raise ValueError('dict_factory: {attr} is required'.format(attr=attrname))

    return objdict


def val_factory(val, datatypes):
    """
    return an instance of `val` that is of type `datatype`.
    keep track of exceptions so we can produce meaningful error messages.
    """
    exceptions = []
    for dt in datatypes:
        try:
            if isinstance(val, dt):
                return val
            return type_handler_object(val, dt)
        except Exception as e:
            exceptions.append(str(e))
    # if we get here, we never found a valid value. raise an error
    raise ValueError('val_factory: Unable to instantiate {val} from types {types}. Exceptions: {excs}'.
                     format(val=val, types=datatypes, excs=exceptions))


def to_json(cls, indent=0):
    """
    serialize to JSON
    :rtype: str
    """
    # for consistency, use as_dict then go to json from there
    return json.dumps(cls.as_dict(), indent=indent)


def to_dict(cls, convert_datetime=True):
    """
    return a dict representation of the Event and its sub-objects
    `convert_datetime` controls whether datetime objects are converted to strings or not
    :rtype: dict
    """

    def todict(obj):
        """
        recurse the objects and represent as a dict
        use the registered handlers if possible
        """
        data = {}
        if isinstance(obj, dict):
            for (key, val) in obj.items():
                data[key] = todict(val)
            return data
        if not convert_datetime and isinstance(obj, datetime):
            return obj
        elif type_handler_value(obj):
            return type_handler_value(obj)
        elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
            return [todict(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if not callable(value) and not key.startswith('_'):
                    data[key] = todict(value)
            return data
        else:
            return obj

    return todict(cls)


class DatetimeHandler(object):
    """
    output datetime objects as iso-8601 compliant strings
    """

    @classmethod
    def flatten(cls, obj):
        """flatten"""
        return timestamp_from_datetime(obj)

    @classmethod
    def restore(cls, data):
        """restore"""
        return timestamp_to_datetime(data)


class UUIDHandler(object):
    """
    output UUID objects as a string
    """

    @classmethod
    def flatten(cls, obj):
        """flatten"""
        return str(obj)

    @classmethod
    def restore(cls, data):
        """restore"""
        return UUID(data)


class EnumHandler(object):
    """
    output Enum objects as their value
    """

    @classmethod
    def flatten(cls, obj):
        """flatten"""
        return obj.value

    @classmethod
    def restore(cls, data):
        """
        cannot restore here because we don't know what type of enum it is
        """
        raise NotImplementedError


handlers = {
    datetime: DatetimeHandler,
    Enum: EnumHandler,
    UUID: UUIDHandler,
}


def handler_for(obj):
    """return the handler for the object type"""
    for handler_type in handlers:
        if isinstance(obj, handler_type):
            return handlers[handler_type]

    try:
        for handler_type in handlers:
            if issubclass(obj, handler_type):
                return handlers[handler_type]
    except TypeError:
        # if obj isn't a class, issubclass will raise a TypeError
        pass


def type_handler_value(obj):
    """
    return the serialized (flattened) value from the registered handler for the type
    """
    handler = handler_for(obj)
    if handler:
        return handler().flatten(obj)


def type_handler_object(val, objtype):
    """
    return the deserialized (restored) value from the registered handler for the type
    """
    handler = handlers.get(objtype)
    if handler:
        return handler().restore(val)
    else:
        return objtype(val)
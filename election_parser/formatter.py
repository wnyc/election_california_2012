import json
import cPickle
import gflags
from decimal import Decimal

FLAGS = gflags.FLAGS


# This is gross ... I really wish json's "default" allowed you to
# process objects that it thought it knew how to encode.  Grrr.

class Converter:
    def __init__(self, **kwargs):
        self.funcs = kwargs

    def dict(self, d):
        newdict = {}
        for k, v in d.items():
            k = self(k)
            v = self(v)
            newdict[k] = v
        return newdict

    def __call__(self, obj):
        if isinstance(obj, dict):
            return self.dict(obj)
        if isinstance(obj, list):
            return map(self, obj)

        if type(obj).__name__ in self.funcs:
            return self.funcs[type(obj).__name__](obj)
        
        return obj
                

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))
        return json.JSONEncoder.default(self, obj)

            
LowPrecisionConverter = Converter(float=lambda x:Decimal("%0.2f" % x))

def low_precision_dumps(obj):
    return json.dumps(LowPrecisionConverter(obj), default=float)
    

FORMATS = {'json':low_precision_dumps,
           'pickle':cPickle.dumps}


gflags.DEFINE_enum('format', 'json', FORMATS.keys(), 'Format to emit')

def dump_factory(format_name):
    return FORMATS[format_name]


def format(data, format=FLAGS.format):
    return dump_factory(format)(data)

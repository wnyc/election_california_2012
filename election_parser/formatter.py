import json
import cPickle
import gflags

FLAGS = gflags.FLAGS

FORMATS = {'json':json.dumps,
           'pickle':cPickle.dumps}

gflags.DEFINE_enum('format', 'json', FORMATS.keys(), 'Format to emit')

def dump_factory(format_name):
    return FORMATS[format_name]


def format(data, format=FLAGS.format):
    return dump_factory(format)(data)

import BaseHTTPServer
import bisect
import gflags
import os
import sys

"""
    This server simulates a web-server that changes with time - files
    in docroot have two parts to their name, the first being a number
    that represents the number of ticks after which that file becomes
    active, and the second part is the actual filename.

    So given the following files in a docroot.

    0000-index.html
    0001-index.html
    0002-index.html

    and a --delay parameter of 60, 0000-index.html will be served for
    index.html for the first 60 seconds, 0001-index.html will be
    served for index.html for the second 60 seconds and so forth.
"""

FLAGS = gflags.FLAGS

from pkg_resources import resource_filename
docroot = resource_filename(__name__, 'data')

gflags.DEFINE_integer('delay', 60, 'Number of seconds between ticks')
gflags.DEFINE_integer('port', 2012, 'Port to listen on')
gflags.DEFINE_string('host', '127.0.0.1', 'Host to bind to')
gflags.DEFINE_string('docroot', docroot, 'Document root - defaults to the package resource for the CA 2012 election test data')


class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
    pass

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

class TimeSensitiveFileLookup:
    def __init__(self, paths, delay=FLAGS.delay):
        """Given a delay and a list of paths return a lookup table.

        Args:
          delay: The length of a tick in seconds
          paths: The filenames from the current docroot
            ['0000-index.html', '0001-index.html', '0002-index.html' ...
        """
        self.files = {}
        for path in paths:
            number, name = path.split('-', 1)
            number = int(number) * delay
            self.files.setdefault(name, []).append((number, False, path))
        for orderings in self.files.values():
            orderings.sort()
        
    def get(self, filename, offset):
        offset = bisect.bisect_right(self.files[filename], (offset, True))
        if offset <= 0:
            offset = 0
        else:
            offset = offset - 1
        return self.files[filename][offset][2]
      
      
    

def main(argv):
    try:
        argv = FLAGS(argv)[1:]
    except gflags.FlagsError, e:
        print "Usage: %s ARGS\\n%s" % (sys.argv[0], FLAGS)
        return 1
    
    server_address = (GFLAGS.host, GFLAGS.port)
    sa = httpd.socket.getsockname()
    log.INFO("Serving HTTP on %s port %s " % tuple(sa))
    
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    httpd.serve_forever()

    
